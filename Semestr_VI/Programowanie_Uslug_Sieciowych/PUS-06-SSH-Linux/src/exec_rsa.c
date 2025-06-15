#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <libssh2.h>
#include "libcommon.h"

#define PASS_LEN 128
#define BUF_SIZE 4096

// #define PUBKEY_FILE "id_rsa.pub"
// #define PRIVKEY_FILE "id_rsa"

// #define PRIVKEY_FILE "/home/wiktor/.ssh/id_rsa"
// #define PUBKEY_FILE "/home/wiktor/.ssh/id_rsa.pub"

#define PRIVKEY_FILE "/home/wiktor/.ssh/id_ed25519"
#define PUBKEY_FILE "/home/wiktor/.ssh/id_ed25519.pub"


int authenticate_user(LIBSSH2_SESSION *session, struct connection_data *cd);

int main(int argc, char **argv) {

    int                 err;
    int                 sockfd;
    char                buf[BUF_SIZE];
    ssize_t             bytes, total;

    struct connection_data  *cd;
    LIBSSH2_SESSION         *session;
    LIBSSH2_CHANNEL         *channel;

    cd = parse_connection_data(argc, argv, CD_ADDRESS | CD_USERNAME);
    if (cd == NULL) {
        exit(EXIT_FAILURE);
    }

    sockfd = establish_tcp_connection(cd);
    if (sockfd == -1) {
        exit(EXIT_FAILURE);
    }

    session = libssh2_session_init();
    if (session == NULL) {
        fprintf(stderr, "libssh2_session_init() failed!\n");
        exit(EXIT_FAILURE);
    }

    libssh2_trace(session, ~0);

    err = libssh2_session_startup(session, sockfd);
    if (err < 0) {
        print_ssh_error(session, "libssh2_session_startup()");
        exit(EXIT_FAILURE);
    }

    err = authenticate_server(session);
    if (err < 0) {
        exit(EXIT_FAILURE);
    }

    err = authenticate_user(session, cd);
    if (err < 0) {
        fprintf(stderr, "Authentication failed!\n");
        exit(EXIT_FAILURE);
    }

    channel = libssh2_channel_open_session(session);
    if (channel == NULL) {
        print_ssh_error(session, "libssh2_channel_open_session()");
        exit(EXIT_FAILURE);
    }

    err = libssh2_channel_exec(channel, "date");
    if (err < 0) {
        print_ssh_error(session, "libssh2_channel_exec()");
        exit(EXIT_FAILURE);
    }

    bytes = total = 0;
    do {
        bytes = libssh2_channel_read(channel, buf + total, BUF_SIZE - total);
        if (bytes > 0) {
             total += bytes;
        }

    } while ((bytes > 0) && (total < BUF_SIZE));

    if (bytes < 0 && bytes != LIBSSH2_ERROR_EAGAIN) {
        print_ssh_error(session, "libssh2_channel_read()");
    }

    fprintf(stdout, "Received:\n");
    fwrite(buf, sizeof(char), total, stdout);
    fprintf(stdout, "\n");

    libssh2_channel_send_eof(channel);
    libssh2_channel_wait_eof(channel);
    libssh2_channel_wait_closed(channel);

    fprintf(stdout, "Exit status: %d\n", libssh2_channel_get_exit_status(channel));

    err = libssh2_channel_close(channel);
    if (err < 0 && err != LIBSSH2_ERROR_CHANNEL_CLOSED) {
        print_ssh_error(session, "libssh2_channel_close()");
    }

    err = libssh2_channel_free(channel);
    if (err < 0) {
        print_ssh_error(session, "libssh2_channel_free()");
    }

    err = libssh2_session_disconnect(session, "Graceful shutdown");
    if (err < 0) {
        print_ssh_error(session, "libssh2_session_disconnect()");
    }

    err = libssh2_session_free(session);

    close(sockfd);

    free_connection_data(cd);

    exit(EXIT_SUCCESS);
}

int authenticate_user(LIBSSH2_SESSION *session, struct connection_data *cd) {

    char *auth_list;
    char passphrase[PASS_LEN];
    int auth_rc;

    auth_list = libssh2_userauth_list(session, cd->username, strlen(cd->username));
    if (auth_list == NULL) {
        if (libssh2_userauth_authenticated(session)) {
            fprintf(stderr, "USERAUTH_NONE succeeded unexpectedly!\n");
            return -1;
        } else {
            print_ssh_error(session, "libssh2_userauth_list()");
            return -1;
        }
    }

    if (strstr(auth_list, "publickey") == NULL) {
        fprintf(stderr, "Public key authentication method not supported by server.\n");
        return -1;
    }

    fprintf(stdout, "Attempting public key authentication with files:\n");
    fprintf(stdout, "  Public key:  %s\n", PUBKEY_FILE);
    fprintf(stdout, "  Private key: %s\n", PRIVKEY_FILE);

    auth_rc = libssh2_userauth_publickey_fromfile_ex(session, cd->username, strlen(cd->username),
                                                     PUBKEY_FILE, PRIVKEY_FILE, NULL);

    if (auth_rc == 0) {
        fprintf(stdout, "Public key authentication succeeded (no passphrase needed or key agent used)!\n");
        return 0;
    }
    else if (auth_rc == LIBSSH2_ERROR_PUBLICKEY_UNVERIFIED || auth_rc == LIBSSH2_ERROR_AUTHENTICATION_FAILED || auth_rc == LIBSSH2_ERROR_PASSWORD_EXPIRED /* Może oznaczać passphrase */) {

        fprintf(stdout, "Initial public key authentication failed (rc: %d). Passphrase might be required.\n", auth_rc);

        for (int retries = 0; retries < 3; ++retries) {

            if (get_password("Private key passphrase (leave blank if none): ", passphrase, PASS_LEN)) {
                fprintf(stderr, "get_password() failed!\n");
                return -1;
            }

            const char *passphrase_to_use = (strlen(passphrase) > 0) ? passphrase : NULL;

            auth_rc = libssh2_userauth_publickey_fromfile_ex(session, cd->username, strlen(cd->username),
                                                             PUBKEY_FILE, PRIVKEY_FILE, passphrase_to_use);

            memset(passphrase, 0, PASS_LEN);

            if (auth_rc == 0) {
                fprintf(stdout, "Public key authentication succeeded!\n");
                return 0;
            } else {
                fprintf(stdout, "Public key authentication failed (rc: %d). Attempt %d/3.\n", auth_rc, retries + 1);
                 if (retries == 2) {
                     print_ssh_error(session, "libssh2_userauth_publickey_fromfile_ex() after retries");
                 }
            }
        }

         fprintf(stderr, "Authentication failed after multiple passphrase attempts.\n");
         return -1;

    } else {
        print_ssh_error(session, "libssh2_userauth_publickey_fromfile_ex()");
        return -1;
    }
}