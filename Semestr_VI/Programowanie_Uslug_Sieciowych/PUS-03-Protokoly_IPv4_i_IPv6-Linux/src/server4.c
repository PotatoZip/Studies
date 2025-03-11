#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char** argv) {
    int listenfd, connfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len;
    char addr_buff[INET_ADDRSTRLEN];
    char message[] = "Laboratorium PUS";

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(atoi(argv[1]));

    if (bind(listenfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %s...\n", argv[1]);

    while (1) {
        client_addr_len = sizeof(client_addr);
        connfd = accept(listenfd, (struct sockaddr*)&client_addr, &client_addr_len);
        if (connfd == -1) {
            perror("accept()");
            continue;
        }

        inet_ntop(AF_INET, &client_addr.sin_addr, addr_buff, sizeof(addr_buff));
        printf("Connection accepted from %s:%d\n", addr_buff, ntohs(client_addr.sin_port));

        send(connfd, message, strlen(message), 0);
        printf("Message sent to client.\n");

        close(connfd);
    }

    close(listenfd);
    return 0;
}
