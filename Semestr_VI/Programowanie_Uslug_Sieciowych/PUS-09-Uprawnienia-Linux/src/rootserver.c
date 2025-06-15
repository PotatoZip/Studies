#define _GNU_SOURCE     /* getresgid() */
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> /* socket() */
#include <netinet/in.h> /* struct sockaddr_in */
#include <arpa/inet.h>  /* inet_ntop() */
#include <unistd.h>     /* close(), setresuid() */
#include <string.h>
#include <errno.h>

int main(int argc, char** argv) {

    int listenfd, connfd;
    struct sockaddr_in client_addr, server_addr;
    socklen_t client_addr_len, server_addr_len;
    char addr_buff[256];
    unsigned int port_number;
    uid_t target_uid;
    uid_t ruid, euid, suid;

    if (argc != 3) {
        fprintf(stderr, "Invocation: %s <PORT> <USER_UID>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    port_number = atoi(argv[1]);
    target_uid = (uid_t) atoi(argv[2]);

    if (port_number < 1024) {
        if (geteuid() != 0) {
            fprintf(stderr, "You need root privileges to bind to well-known port (<1024).\n");
            exit(EXIT_FAILURE);
        }
    }

    listenfd = socket(PF_INET, SOCK_STREAM, 0);
    if (listenfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port_number);
    server_addr_len = sizeof(server_addr);

    if (getresuid(&ruid, &euid, &suid) == -1) {
        perror("getresuid()");
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "Before bind - UID: %u, EUID: %u, SUID: %u\n", ruid, euid, suid);

    fprintf(stdout, "Binding to port %u...\n", port_number);
    if (bind(listenfd, (struct sockaddr*) &server_addr, server_addr_len) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    // **Zmiana identyfikatorów na zwykłego użytkownika (target_uid)**
    if (setresuid(target_uid, target_uid, target_uid) == -1) {
        perror("setresuid()");
        exit(EXIT_FAILURE);
    }

    if (getresuid(&ruid, &euid, &suid) == -1) {
        perror("getresuid()");
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "After setresuid - UID: %u, EUID: %u, SUID: %u\n", ruid, euid, suid);

    if (euid == 0 || suid == 0) {
        fprintf(stderr, "Run server as unprivileged user after privilege drop!\n");
        exit(EXIT_FAILURE);
    }

    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "Server is listening for incoming connection...\n");

    client_addr_len = sizeof(client_addr);
    connfd = accept(listenfd, (struct sockaddr*)&client_addr, &client_addr_len);
    if (connfd == -1) {
        perror("accept()");
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "TCP connection accepted from %s:%d\n",
        inet_ntop(AF_INET, &client_addr.sin_addr, addr_buff, sizeof(addr_buff)),
        ntohs(client_addr.sin_port));

    sleep(5);

    fprintf(stdout, "Closing connected socket (sending FIN to client)...\n");
    close(connfd);
    close(listenfd);

    exit(EXIT_SUCCESS);
}
