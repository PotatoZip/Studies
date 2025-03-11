#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int main(int argc, char** argv) {
    int listenfd, connfd;
    struct sockaddr_in6 server_addr, client_addr;
    socklen_t client_addr_len;
    char addr_buff[INET6_ADDRSTRLEN];
    char message[] = "Laboratorium PUS";

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    listenfd = socket(AF_INET6, SOCK_STREAM, 0);
    if (listenfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin6_family = AF_INET6;
    server_addr.sin6_addr = in6addr_any;
    server_addr.sin6_port = htons(atoi(argv[1]));

    if (bind(listenfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening for incoming connections...\n");

    while (1) {
        client_addr_len = sizeof(client_addr);
        connfd = accept(listenfd, (struct sockaddr*)&client_addr, &client_addr_len);
        if (connfd == -1) {
            perror("accept()");
            continue;
        }

        inet_ntop(AF_INET6, &client_addr.sin6_addr, addr_buff, sizeof(addr_buff));
        printf("Connection accepted from %s:%d\n",
               addr_buff, ntohs(client_addr.sin6_port));

        if (IN6_IS_ADDR_V4MAPPED(&client_addr.sin6_addr)) {
            printf("Client is using an IPv4-mapped IPv6 address.\n");
        } else {
            printf("Client is using a native IPv6 address.\n");
        }

        send(connfd, message, strlen(message), 0);
        printf("Message sent to client.\n");

        close(connfd);
    }

    close(listenfd);
    return 0;
}
