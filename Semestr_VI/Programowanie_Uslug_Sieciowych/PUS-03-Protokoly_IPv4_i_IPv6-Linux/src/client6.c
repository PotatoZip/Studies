#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <net/if.h>

int main(int argc, char** argv) {
    int sockfd;
    struct sockaddr_in6 server_addr;
    char buff[256];
    int retval;
    unsigned int if_index;

    if (argc != 4) {
        fprintf(stderr, "Usage: %s <IPv6 ADDRESS> <PORT> <INTERFACE>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if_index = if_nametoindex(argv[3]);
    if (if_index == 0) {
        perror("if_nametoindex()");
        exit(EXIT_FAILURE);
    }

    sockfd = socket(AF_INET6, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin6_family = AF_INET6;
    server_addr.sin6_port = htons(atoi(argv[2]));

    retval = inet_pton(AF_INET6, argv[1], &server_addr.sin6_addr);
    if (retval == 0) {
        fprintf(stderr, "inet_pton(): Invalid IPv6 address!\n");
        exit(EXIT_FAILURE);
    } else if (retval == -1) {
        perror("inet_pton()");
        exit(EXIT_FAILURE);
    }

    server_addr.sin6_scope_id = if_index;

    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect()");
        exit(EXIT_FAILURE);
    }

    printf("Connected to server. Waiting for message...\n");

    retval = recv(sockfd, buff, sizeof(buff) - 1, 0);
    if (retval == -1) {
        perror("recv()");
        exit(EXIT_FAILURE);
    }
    buff[retval] = '\0';

    printf("Received message: '%s'\n", buff);

    close(sockfd);

    return 0;
}
