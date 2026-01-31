#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> /* socket() */
#include <netinet/in.h> /* struct sockaddr_in */
#include <arpa/inet.h>  /* inet_ntop() */
#include <unistd.h>     /* close() */
#include <string.h>
#include <errno.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/err.h>
#include <openssl/crypto.h> // Dla CRYPTO_memcmp

// --- Stałe kryptograficzne (MUSZĄ być takie same w kliencie!) ---
// Klucz AES (16 bajtów dla AES-128)
unsigned char aes_key[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
                           0x00,0x01,0x02,0x03,0x04,0x05};
// Wektor IV (16 bajtów dla AES-CBC)
unsigned char iv[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
                      0x00,0x01,0x02,0x03,0x04,0x05};
// Klucz HMAC
unsigned char hmac_key[] = "sekretny_klucz_hmac_pus"; // Ten sam co w kliencie
const int hmac_key_len = sizeof(hmac_key) - 1;
const EVP_MD *hmac_md = NULL;
#define HMAC_DIGEST EVP_sha256
unsigned int hmac_len_expected = 0; // Oczekiwana długość HMAC (ustawiana po inicjalizacji)
// --- Koniec stałych kryptograficznych ---

#define MAX_BUFF_SIZE 256

void handle_openssl_error(void) {
    ERR_print_errors_fp(stderr);
    exit(EXIT_FAILURE);
}

int main(int argc, char** argv) {

    int             sockfd;           /* Deskryptor gniazda. */
    int             retval;           /* Wartosc zwracana przez funkcje. */
    struct          sockaddr_in client_addr, server_addr;
    socklen_t       client_addr_len, server_addr_len;
    unsigned char   buff[MAX_BUFF_SIZE]; // Zmieniono typ na unsigned char
    char            addr_buff[INET_ADDRSTRLEN]; // INET_ADDRSTRLEN jest bezpieczniejsze

    unsigned char   *received_ciphertext = NULL;
    int             received_ciphertext_len = 0;
    unsigned char   *received_hmac = NULL;

    unsigned char   calculated_hmac[EVP_MAX_MD_SIZE];
    unsigned int    calculated_hmac_len = 0;

    unsigned char   decrypted_plaintext[MAX_BUFF_SIZE];
    int             decrypted_len = 0;
    int             len_update = 0, len_final = 0;

    EVP_CIPHER_CTX  *ctx_dec;

    if (argc != 2) {
        fprintf(stderr, "Invocation: %s <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Inicjalizacja OpenSSL
    ERR_load_crypto_strings();
    // OpenSSL_add_all_digests();
    hmac_md = HMAC_DIGEST();
    hmac_len_expected = EVP_MD_size(hmac_md); // Pobierz oczekiwaną długość HMAC dla SHA256 (32)

    sockfd = socket(PF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port        = htons(atoi(argv[1]));
    server_addr_len             = sizeof(server_addr);

    if (bind(sockfd, (struct sockaddr*) &server_addr, server_addr_len) == -1) {
        perror("bind()");
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "Server is waiting for UDP datagram on port %s...\n", argv[1]);

    client_addr_len = sizeof(client_addr);

    retval = recvfrom(sockfd, buff, sizeof(buff), 0,
                      (struct sockaddr*)&client_addr, &client_addr_len);
    if (retval == -1) {
        perror("recvfrom()");
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "\nUDP datagram received from %s:%d (%d bytes).\n",
            inet_ntop(AF_INET, &client_addr.sin_addr, addr_buff, sizeof(addr_buff)),
            ntohs(client_addr.sin_port),
            retval
           );

    // --- Separacja danych i weryfikacja HMAC ---
    if (retval < hmac_len_expected) {
        fprintf(stderr, "Error: Received data is too short to contain HMAC (%d < %d)\n", retval, hmac_len_expected);
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    received_ciphertext_len = retval - hmac_len_expected;
    received_ciphertext = buff; // Ciphertext jest na początku bufora
    received_hmac = buff + received_ciphertext_len; // HMAC jest na końcu

    // Oblicz HMAC dla otrzymanego szyfrogramu
    if (HMAC(hmac_md, hmac_key, hmac_key_len, received_ciphertext, received_ciphertext_len, calculated_hmac, &calculated_hmac_len) == NULL) {
        fprintf(stderr, "HMAC calculation failed on server\n");
        handle_openssl_error();
    }

    // Porównaj HMAC (bezpieczne porównanie!)
    if (calculated_hmac_len == hmac_len_expected &&
        CRYPTO_memcmp(calculated_hmac, received_hmac, hmac_len_expected) == 0)
    {
        fprintf(stdout, "HMAC verification successful!\n");

        // --- Deszyfrowanie (tylko jeśli HMAC jest poprawny) ---
        if (!(ctx_dec = EVP_CIPHER_CTX_new())) handle_openssl_error();

        // Inicjalizacja deszyfrowania
        if (!EVP_DecryptInit_ex(ctx_dec, EVP_aes_128_cbc(), NULL, aes_key, iv)) handle_openssl_error();

        // Włączenie usuwania dopełniania
        if (!EVP_CIPHER_CTX_set_padding(ctx_dec, 1)) handle_openssl_error();

        // Deszyfrowanie (Update)
        if (!EVP_DecryptUpdate(ctx_dec, decrypted_plaintext, &len_update, received_ciphertext, received_ciphertext_len)) {
            fprintf(stderr, "Decryption update failed (maybe wrong key/IV or corrupted data?)\n");
            handle_openssl_error(); // Pokaże błędy OpenSSL
        }
        decrypted_len = len_update;

        // Finalizacja deszyfrowania (sprawdzenie i usunięcie dopełnienia)
        if (!EVP_DecryptFinal_ex(ctx_dec, decrypted_plaintext + len_update, &len_final)) {
            fprintf(stderr, "Decryption final failed (likely padding error - wrong key or corrupted data)\n");
            handle_openssl_error(); // Pokaże błędy OpenSSL
        } else {
             decrypted_len += len_final;
             fprintf(stdout, "Decrypted message: %.*s\n", decrypted_len, decrypted_plaintext);
        }

        EVP_CIPHER_CTX_free(ctx_dec); // Zwolnienie kontekstu

    } else {
        fprintf(stderr, "HMAC verification FAILED! Message rejected.\n");
        // Nie deszyfrujemy, jeśli HMAC jest niepoprawny
    }


    close(sockfd);
    ERR_free_strings();
    // EVP_cleanup();

    exit(EXIT_SUCCESS);
}