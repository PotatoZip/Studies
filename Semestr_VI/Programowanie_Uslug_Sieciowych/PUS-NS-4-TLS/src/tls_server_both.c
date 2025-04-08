#include <errno.h>
#include <unistd.h>
#include <malloc.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <resolv.h>
#include "openssl/ssl.h"
#include "openssl/err.h"

const char* MESSAGE = "Laboratorium PUS.";

void ShowCerts(SSL* ssl) {
    X509 *cert = SSL_get_peer_certificate(ssl);
    if (cert != NULL) {
        printf("Client certificates:\n");
        char *line = X509_NAME_oneline(X509_get_subject_name(cert), 0, 0);
        printf("Subject: %s\n", line);
        free(line);
        line = X509_NAME_oneline(X509_get_issuer_name(cert), 0, 0);
        printf("Issuer: %s\n", line);
        free(line);
        X509_free(cert);
    } else {
        printf("No client certificate provided.\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <portnum>\n", argv[0]);
        return 1;
    }
    int port = atoi(argv[1]);

    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();

    SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
    if (!ctx) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Załadowanie certyfikatu i klucza serwera
    if (SSL_CTX_use_certificate_file(ctx, "server_chain.pem", SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, "server_keypair.pem", SSL_FILETYPE_PEM) <= 0) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Weryfikacja klucza prywatnego
    if (!SSL_CTX_check_private_key(ctx)) {
        fprintf(stderr, "Private key does not match certificate\n");
        return 1;
    }

    // Załadowanie katalogu z certyfikatami CA
    if (SSL_CTX_load_verify_locations(ctx, NULL, "cert_dir") != 1) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Wymuszanie uwierzytelnienia klienta
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);

    int server = socket(PF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;
    bzero(&addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server, (struct sockaddr*)&addr, sizeof(addr)) != 0 || listen(server, 10) != 0) {
        perror("bind/listen");
        return 1;
    }

    while (1) {
        struct sockaddr_in addr;
        socklen_t len = sizeof(addr);
        int client = accept(server, (struct sockaddr*)&addr, &len);
        printf("Connection: %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

        SSL *ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client);

        if (SSL_accept(ssl) > 0) {
            ShowCerts(ssl);
            SSL_write(ssl, MESSAGE, strlen(MESSAGE));
            SSL_shutdown(ssl);
        } else {
            ERR_print_errors_fp(stderr);
        }

        SSL_free(ssl);
        close(client);
    }

    close(server);
    SSL_CTX_free(ctx);
    return 0;
}
