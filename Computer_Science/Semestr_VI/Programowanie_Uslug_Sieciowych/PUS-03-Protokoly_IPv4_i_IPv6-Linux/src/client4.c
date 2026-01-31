#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int main(int argc, char** argv) {
    int sockfd;
    struct sockaddr_in server_addr;
    char buff[256];
    int retval;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <IPv4 ADDRESS> <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(atoi(argv[2]));

    retval = inet_pton(AF_INET, argv[1], &server_addr.sin_addr);
    if (retval == 0) {
        fprintf(stderr, "inet_pton(): Invalid IPv4 address!\n");
        exit(EXIT_FAILURE);
    } else if (retval == -1) {
        perror("inet_pton()");
        exit(EXIT_FAILURE);
    }

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
