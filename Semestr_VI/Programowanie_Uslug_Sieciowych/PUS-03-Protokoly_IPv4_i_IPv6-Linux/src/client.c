#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int sockfd;
    struct addrinfo hints, *res, *rp;
    int retval;
    struct sockaddr_storage local_addr;
    socklen_t addr_len;
    char local_ip[NI_MAXHOST], local_port[NI_MAXSERV];
    char buff[256];

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <IPv4 or IPv6 address> <Port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = 0;

    retval = getaddrinfo(argv[1], argv[2], &hints, &res);
    if (retval != 0) {
        fprintf(stderr, "getaddrinfo(): %s\n", gai_strerror(retval));
        exit(EXIT_FAILURE);
    }

    for (rp = res; rp != NULL; rp = rp->ai_next) {
        sockfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (sockfd == -1) continue;

        if (connect(sockfd, rp->ai_addr, rp->ai_addrlen) != -1) {
            break;
        }

        close(sockfd);
    }

    if (rp == NULL) {
        fprintf(stderr, "Could not connect to server\n");
        exit(EXIT_FAILURE);
    }

    freeaddrinfo(res);

    addr_len = sizeof(local_addr);
    if (getsockname(sockfd, (struct sockaddr *)&local_addr, &addr_len) == -1) {
        perror("getsockname()");
        exit(EXIT_FAILURE);
    }

    retval = getnameinfo((struct sockaddr *)&local_addr, addr_len,
                         local_ip, NI_MAXHOST, local_port, NI_MAXSERV,
                         NI_NUMERICHOST | NI_NUMERICSERV);
    if (retval != 0) {
        fprintf(stderr, "getnameinfo(): %s\n", gai_strerror(retval));
        exit(EXIT_FAILURE);
    }

    printf("Connected to server.\n");
    printf("Local IP: %s, Local Port: %s\n", local_ip, local_port);

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
