#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/capability.h>

int drop_all_caps() {
    cap_t caps = cap_init();
    if (caps == NULL) {
        perror("cap_init()");
        return -1;
    }
    if (cap_set_proc(caps) == -1) {
        perror("cap_set_proc()");
        cap_free(caps);
        return -1;
    }
    cap_free(caps);
    return 0;
}

int main(int argc, char **argv) {
    int listenfd, connfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len;
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

    printf("Binding to port %u...\n", port_number);
    if (bind(listenfd, (struct sockaddr *) &server_addr, sizeof(server_addr)) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    /* Zrzucenie wszystkich uprawnień po bind() */
    if (drop_all_caps() == -1) {
        fprintf(stderr, "Failed to drop capabilities\n");
        exit(EXIT_FAILURE);
    }

    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening...\n");

    client_addr_len = sizeof(client_addr);
    connfd = accept(listenfd, (struct sockaddr *) &client_addr, &client_addr_len);
    if (connfd == -1) {
        perror("accept()");
        exit(EXIT_FAILURE);
    }

    printf("Accepted connection from %s:%d\n",
           inet_ntop(AF_INET, &client_addr.sin_addr, addr_buff, sizeof(addr_buff)),
           ntohs(client_addr.sin_port));

    sleep(5);
    printf("Closing connection...\n");

    close(connfd);
    close(listenfd);
    return EXIT_SUCCESS;
}
