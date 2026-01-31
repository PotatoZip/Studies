#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Użycie: %s <adres IP> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int sockfd;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE];

    // Tworzenie gniazda UDP
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    // Konfiguracja adresu serwera
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(argv[2]));
    if (inet_pton(AF_INET, argv[1], &serv_addr.sin_addr) <= 0) {
        perror("Błędny adres IP");
        exit(EXIT_FAILURE);
    }

    // Połączenie gniazda z adresem serwera
    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Błąd łączenia");
        exit(EXIT_FAILURE);
    }

    while (1) {
        printf("Wpisz wiadomość: ");
        fgets(buffer, BUFFER_SIZE, stdin);

        // Usuwanie nowej linii
        buffer[strcspn(buffer, "\n")] = 0;

        // Wysłanie pustego datagramu kończy program
        if (strlen(buffer) == 0) {
            send(sockfd, "", 0, 0);
            break;
        }

        // Wysłanie wiadomości do serwera
        if (send(sockfd, buffer, strlen(buffer), 0) < 0) {
            perror("Błąd wysyłania");
            break;
        }

        // Odbiór odpowiedzi od serwera
        int recv_len = recv(sockfd, buffer, BUFFER_SIZE, 0);
        if (recv_len < 0) {
            perror("Błąd odbierania");
            break;
        }

        buffer[recv_len] = '\0';
        printf("Serwer: %s\n", buffer);
    }

    close(sockfd);
    return 0;
}
