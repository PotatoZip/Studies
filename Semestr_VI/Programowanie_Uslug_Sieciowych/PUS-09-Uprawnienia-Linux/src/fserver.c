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
    struct sockaddr_in client_addr, server_addr;
    socklen_t client_addr_len, server_addr_len;
    char addr_buff[256];
    unsigned int port_number;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    port_number = atoi(argv[1]);

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

    printf("Binding to port %u...\n", port_number);
    if (bind(listenfd, (struct sockaddr*) &server_addr, server_addr_len) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening for incoming connection...\n");

    client_addr_len = sizeof(client_addr);
    connfd = accept(listenfd, (struct sockaddr*)&client_addr, &client_addr_len);
    if (connfd == -1) {
        perror("accept()");
        exit(EXIT_FAILURE);
    }

    printf("TCP connection accepted from %s:%d\n",
        inet_ntop(AF_INET, &client_addr.sin_addr, addr_buff, sizeof(addr_buff)),
        ntohs(client_addr.sin_port));

    sleep(5);

    printf("Closing connected socket...\n");
    close(connfd);
    close(listenfd);

    return EXIT_SUCCESS;
}
