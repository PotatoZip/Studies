#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <sys/time.h>
#include <sys/types.h>
#include <fcntl.h>
#include <netdb.h>
#include <libssh2.h>
#include "libcommon.h"

#define LISTEN_BACKLOG 5
#define BUF_SIZE 4096
#define PASS_LEN 128

int forward_data(int client_sock, LIBSSH2_CHANNEL *channel, LIBSSH2_SESSION *session);

int authenticate_user_password(LIBSSH2_SESSION *session, const char *username);

int main(int argc, char **argv) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <local_port> <target_host> <target_port> <user@ssh_server_host>\n", argv[0]);
        fprintf(stderr, "Example: %s 8080 webserver.internal.com 80 user@jumphost.example.com\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    long local_port_long = strtol(argv[1], NULL, 10);
    if (local_port_long <= 0 || local_port_long > 65535) {
        fprintf(stderr, "Invalid local port: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    unsigned short local_port = (unsigned short)local_port_long;
    const char *target_host = argv[2];
    long target_port_long = strtol(argv[3], NULL, 10);
     if (target_port_long <= 0 || target_port_long > 65535) {
        fprintf(stderr, "Invalid target port: %s\n", argv[3]);
        exit(EXIT_FAILURE);
    }
    unsigned short target_port = (unsigned short)target_port_long;
    char *ssh_connect_str = argv[4];
    char *ssh_user = ssh_connect_str;
    char *ssh_host = strchr(ssh_connect_str, '@');
    if (!ssh_host) {
        fprintf(stderr, "Invalid format for user@ssh_server_host: %s\n", ssh_connect_str);
        exit(EXIT_FAILURE);
    }
    *ssh_host = '\0';
    ssh_host++;

    int err;
    int listen_sock = -1, client_sock = -1, ssh_sock = -1;
    LIBSSH2_SESSION *session = NULL;
    LIBSSH2_CHANNEL *channel = NULL;

    struct sockaddr_in listen_addr;
    int on = 1;

    err = libssh2_init(0);
    if (err != 0) {
        fprintf(stderr, "libssh2 initialization failed (%d)\n", err);
        return 1;
    }

    struct addrinfo hints, *res, *rp;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    err = getaddrinfo(ssh_host, "22", &hints, &res);
    if (err != 0) {
        fprintf(stderr, "getaddrinfo for %s failed: %s\n", ssh_host, gai_strerror(err));
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    for (rp = res; rp != NULL; rp = rp->ai_next) {
        ssh_sock = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (ssh_sock == -1) {
            perror("socket() for SSH connection failed");
            continue;
        }

        fprintf(stdout, "Connecting to SSH server %s:%d...\n", ssh_host, 22);
        if (connect(ssh_sock, rp->ai_addr, rp->ai_addrlen) == 0) {
            break;
        } else {
             perror("connect() to SSH server failed");
             close(ssh_sock);
             ssh_sock = -1;
        }
    }

    freeaddrinfo(res);

    if (ssh_sock == -1) {
        fprintf(stderr, "Could not connect to SSH server %s\n", ssh_host);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "Connected to SSH server.\n");

    session = libssh2_session_init();
    if (!session) {
        fprintf(stderr, "libssh2_session_init failed\n");
        close(ssh_sock);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    err = libssh2_session_handshake(session, ssh_sock);
    if (err) {
        print_ssh_error(session, "SSH handshake failed");
        libssh2_session_free(session);
        close(ssh_sock);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "SSH handshake completed.\n");

    if (authenticate_user_password(session, ssh_user) != 0) {
        fprintf(stderr, "SSH Authentication Failed\n");
        libssh2_session_disconnect(session, "Auth failed");
        libssh2_session_free(session);
        close(ssh_sock);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "SSH Authentication Successful for user %s.\n", ssh_user);

    listen_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_sock == -1) {
        perror("socket() for listener failed");
        goto shutdown;
    }

    setsockopt(listen_sock, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));

    memset(&listen_addr, 0, sizeof(listen_addr));
    listen_addr.sin_family = AF_INET;
    listen_addr.sin_port = htons(local_port);
    listen_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (bind(listen_sock, (struct sockaddr*)&listen_addr, sizeof(listen_addr)) < 0) {
        perror("bind() failed");
        goto shutdown;
    }

    if (listen(listen_sock, LISTEN_BACKLOG) < 0) {
        perror("listen() failed");
        goto shutdown;
    }

    fprintf(stdout, "Listening on 127.0.0.1:%d... Forwarding to %s:%d via %s@%s\n",
            local_port, target_host, target_port, ssh_user, ssh_host);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);

        fprintf(stdout, "Waiting for connection on local port %d...\n", local_port);
        client_sock = accept(listen_sock, (struct sockaddr*)&client_addr, &client_addr_len);
        if (client_sock < 0) {
            perror("accept() failed");
            goto shutdown;
        }
        fprintf(stdout, "Client connected from %s:%d\n",
                inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        fprintf(stdout, "Requesting direct-tcpip channel to %s:%d...\n", target_host, target_port);

        channel = libssh2_channel_direct_tcpip_ex(session, target_host, target_port,
                                                    "127.0.0.1", 0);

        if (!channel) {
            int last_errno = libssh2_session_last_errno(session);
             fprintf(stderr, "Could not open direct-tcpip channel (error %d)\n", last_errno);
            if (last_errno == LIBSSH2_ERROR_EAGAIN) {
                fprintf(stderr, "Try again later (EAGAIN)\n");
            } else {
                 print_ssh_error(session, "libssh2_channel_direct_tcpip_ex failed");
            }
            close(client_sock);
            client_sock = -1;
            continue;
        }
        fprintf(stdout, "Direct-tcpip channel established. Forwarding data...\n");

        forward_data(client_sock, channel, session);

        fprintf(stdout, "Closing channel and client connection.\n");
        if (channel) {
            libssh2_channel_send_eof(channel);
            libssh2_channel_wait_eof(channel);
            libssh2_channel_wait_closed(channel);
            libssh2_channel_free(channel);
            channel = NULL;
        }
        if (client_sock != -1) {
            close(client_sock);
            client_sock = -1;
        }
    }


shutdown:
    fprintf(stdout, "Shutting down...\n");
    if (listen_sock != -1) close(listen_sock);
    if (client_sock != -1) close(client_sock);
    if (channel) libssh2_channel_free(channel);
    if (session) {
        libssh2_session_disconnect(session, "Normal shutdown");
        libssh2_session_free(session);
    }
    if (ssh_sock != -1) close(ssh_sock);
    libssh2_exit();
    return 0;
}

int forward_data(int client_sock, LIBSSH2_CHANNEL *channel, LIBSSH2_SESSION *session) {
    fd_set read_fds;
    struct timeval tv;
    int rc;
    char buf[BUF_SIZE];
    ssize_t nread, nwritten;
    int ssh_fd = libssh2_session_get_fd(session);

    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(client_sock, &read_fds);
        FD_SET(ssh_fd, &read_fds);

        int max_fd = (client_sock > ssh_fd) ? client_sock : ssh_fd;

        tv.tv_sec = 1;
        tv.tv_usec = 0;

        rc = select(max_fd + 1, &read_fds, NULL, NULL, &tv);
        if (rc < 0) {
            perror("select() failed");
            return -1;
        } else if (rc == 0) {
            if (libssh2_channel_eof(channel)) {
                 fprintf(stderr, "Channel EOF detected during timeout.\n");
                 break;
            }
            continue;
        }

        if (FD_ISSET(client_sock, &read_fds)) {
            nread = read(client_sock, buf, BUF_SIZE);
            if (nread < 0) {
                if (errno == EAGAIN || errno == EWOULDBLOCK) {
                } else {
                    perror("read() from client failed");
                    return -1;
                }
            } else if (nread == 0) {
                fprintf(stdout, "Client disconnected (EOF).\n");
                return 0;
            } else {
                nwritten = libssh2_channel_write(channel, buf, nread);
                 if (nwritten < 0) {
                    if (nwritten == LIBSSH2_ERROR_EAGAIN) {
                        fprintf(stderr, "libssh2_channel_write: EAGAIN - should retry\n");
                    } else {
                        print_ssh_error(session, "libssh2_channel_write failed");
                        return -1;
                    }
                } else if (nwritten != nread) {
                    fprintf(stderr, "Warning: short write to libssh2 channel (%zd/%zd)\n", nwritten, nread);
                }
            }
        }

        if (FD_ISSET(ssh_fd, &read_fds)) {
            nread = libssh2_channel_read(channel, buf, BUF_SIZE);
             if (nread < 0) {
                if (nread == LIBSSH2_ERROR_EAGAIN) {
                } else {
                    print_ssh_error(session, "libssh2_channel_read failed");
                    return -1;
                }
            } else if (nread == 0) {
                 fprintf(stdout, "Remote end closed connection (EOF on channel).\n");
                 return 0;
             } else {
                 nwritten = write(client_sock, buf, nread);
                 if (nwritten < 0) {
                     perror("write() to client failed");
                     return -1;
                 } else if (nwritten != nread) {
                      fprintf(stderr, "Warning: short write to client socket (%zd/%zd)\n", nwritten, nread);
                 }
             }
        }

         if (libssh2_channel_eof(channel)) {
              fprintf(stdout, "Remote end closed connection (EOF detected).\n");
              break;
         }

    }

    return 0;
}


int authenticate_user_password(LIBSSH2_SESSION *session, const char *username) {
    char password[PASS_LEN];
    int auth_rc;

    fprintf(stdout, "Attempting password authentication for user %s...\n", username);
    for (int attempts = 0; attempts < 3; ++attempts) {
        if (get_password("Password: ", password, PASS_LEN)) {
            fprintf(stderr, "get_password() failed!\n");
            memset(password, 0, PASS_LEN);
            return -1;
        }

        auth_rc = libssh2_userauth_password(session, username, password);
        memset(password, 0, PASS_LEN);

        if (auth_rc == 0) {
            return 0;
        } else if (auth_rc == LIBSSH2_ERROR_EAGAIN) {
             fprintf(stderr, "Password auth error: Non-blocking I/O, try again.\n");
        } else if (auth_rc == LIBSSH2_ERROR_AUTHENTICATION_FAILED) {
             fprintf(stderr, "Authentication failed! (Attempt %d/3)\n", attempts + 1);
        } else {
             print_ssh_error(session, "Password authentication error");
             return -1;
        }
    }
    fprintf(stderr, "Password authentication failed after 3 attempts.\n");
    return -1;
}