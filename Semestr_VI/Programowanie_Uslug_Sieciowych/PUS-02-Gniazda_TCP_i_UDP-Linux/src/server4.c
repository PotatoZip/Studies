#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <fcntl.h>

#define BUFFER_SIZE 1024
#define MAX_CLIENTS 10

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Użycie: %s <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int server_fd, new_client, max_fd, activity, valread;
    int client_sockets[MAX_CLIENTS] = {0};
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    fd_set read_fds;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(atoi(argv[1]));

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Błąd bindowania");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, MAX_CLIENTS) < 0) {
        perror("Błąd nasłuchiwania");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Serwer nasłuchuje na porcie %s...\n", argv[1]);

    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(server_fd, &read_fds);
        max_fd = server_fd;

        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (client_sockets[i] > 0) {
                FD_SET(client_sockets[i], &read_fds);
            }
            if (client_sockets[i] > max_fd) {
                max_fd = client_sockets[i];
            }
        }

        activity = select(max_fd + 1, &read_fds, NULL, NULL, NULL);
        if ((activity < 0) && (errno != EINTR)) {
            perror("Błąd select()");
        }

        if (FD_ISSET(server_fd, &read_fds)) {
            if ((new_client = accept(server_fd, (struct sockaddr*)&client_addr, &addr_len)) < 0) {
                perror("Błąd akceptowania nowego połączenia");
                continue;
            }

            char client_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
            printf("Nowe połączenie: %s:%d\n", client_ip, ntohs(client_addr.sin_port));

            for (int i = 0; i < MAX_CLIENTS; i++) {
                if (client_sockets[i] == 0) {
                    client_sockets[i] = new_client;
                    break;
                }
            }
        }

        for (int i = 0; i < MAX_CLIENTS; i++) {
            int sock = client_sockets[i];
            if (FD_ISSET(sock, &read_fds)) {
                valread = read(sock, buffer, BUFFER_SIZE);
                if (valread == 0) {
                    getpeername(sock, (struct sockaddr*)&client_addr, &addr_len);
                    printf("Rozłączono klienta: %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

                    close(sock);
                    client_sockets[i] = 0;
                } else {
                    buffer[valread] = '\0';
                    printf("Otrzymano: %s", buffer);

                    for (int j = 0; j < MAX_CLIENTS; j++) {
                        if (client_sockets[j] != 0 && client_sockets[j] != sock) {
                            send(client_sockets[j], buffer, valread, 0);
                        }
                    }
                }
            }
        }
    }

    close(server_fd);
    return 0;
}
