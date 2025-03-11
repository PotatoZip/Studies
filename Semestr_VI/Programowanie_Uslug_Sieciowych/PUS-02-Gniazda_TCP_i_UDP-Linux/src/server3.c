#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "libpalindrome.h"

#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Użycie: %s <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int sockfd;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t cli_len = sizeof(cli_addr);
    char buffer[BUFFER_SIZE];

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    if (bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Błąd bindowania");
        exit(EXIT_FAILURE);
    }

    printf("Serwer UDP nasłuchuje na porcie %s...\n", argv[1]);

    while (1) {
        memset(buffer, 0, BUFFER_SIZE);

        int recv_len = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&cli_addr, &cli_len);
        if (recv_len < 0) {
            perror("Błąd odbioru");
            continue;
        }

        if (recv_len == 0) {
            printf("Otrzymano pusty datagram. Zamykam serwer.\n");
            break;
        }

        buffer[recv_len] = '\0';

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &cli_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
        printf("Otrzymano od %s:%d - \"%s\"\n", client_ip, ntohs(cli_addr.sin_port), buffer);

        if (is_palindrome(buffer, recv_len) == 1) {
            snprintf(buffer, BUFFER_SIZE, "TAK, to palindrom");
        } else {
            snprintf(buffer, BUFFER_SIZE, "NIE, to nie jest palindrom");
        }

        if (sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr*)&cli_addr, cli_len) < 0) {
            perror("Błąd wysyłania");
        }
    }

    close(sockfd);
    return 0;
}
