#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> /* socket() */
#include <netinet/in.h> /* struct sockaddr_in */
#include <arpa/inet.h>  /* inet_pton() */
#include <unistd.h>     /* close() */
#include <string.h>
#include <errno.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/err.h>

// --- Stałe kryptograficzne (MUSZĄ być takie same w serwerze!) ---
// Klucz AES (16 bajtów dla AES-128)
unsigned char aes_key[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
                           0x00,0x01,0x02,0x03,0x04,0x05};
// Wektor IV (16 bajtów dla AES-CBC)
unsigned char iv[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
                      0x00,0x01,0x02,0x03,0x04,0x05};
// Klucz HMAC (długość dowolna, ale zalecana co najmniej długość skrótu)
unsigned char hmac_key[] = "sekretny_klucz_hmac_pus"; // Przykład
const int hmac_key_len = sizeof(hmac_key) - 1; // Długość klucza HMAC
const EVP_MD *hmac_md = NULL; // Wskaźnik na algorytm skrótu dla HMAC
#define HMAC_DIGEST EVP_sha256 // Wybór algorytmu skrótu dla HMAC
// --- Koniec stałych kryptograficznych ---

#define MAX_BUFF_SIZE 256 // Maksymalny rozmiar bufora wysyłania/odbioru

void handle_openssl_error(void) {
    ERR_print_errors_fp(stderr);
    exit(EXIT_FAILURE);
}

int main(int argc, char** argv) {

    int             sockfd;           /* Deskryptor gniazda. */
    int             retval;           /* Wartosc zwracana przez funkcje. */
    struct          sockaddr_in remote_addr;/* Gniazdowa struktura adresowa. */
    socklen_t       addr_len;         /* Rozmiar struktury w bajtach. */

    char            plaintext[] = "Laboratorium PUS."; // Wiadomość do wysłania
    int             plaintext_len = strlen(plaintext);

    unsigned char   ciphertext[MAX_BUFF_SIZE]; // Bufor na szyfrogram
    int             ciphertext_len = 0;
    int             len_update = 0, len_final = 0;

    unsigned char   hmac_result[EVP_MAX_MD_SIZE]; // Bufor na wynik HMAC
    unsigned int    hmac_len = 0;

    unsigned char   send_buffer[MAX_BUFF_SIZE]; // Bufor do wysłania (ciphertext + hmac)
    int             total_payload_len = 0;

    EVP_CIPHER_CTX  *ctx_enc;

    if (argc != 3) {
        fprintf(stderr, "Invocation: %s <IPv4 ADDRESS> <PORT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Inicjalizacja OpenSSL
    ERR_load_crypto_strings();
    // OpenSSL_add_all_digests(); // W nowszych wersjach nie zawsze potrzebne
    hmac_md = HMAC_DIGEST(); // Pobranie EVP_MD dla HMAC

    // --- Szyfrowanie ---
    if (!(ctx_enc = EVP_CIPHER_CTX_new())) handle_openssl_error();

    // Inicjalizacja szyfrowania: AES-128-CBC, klucz, IV
    if (!EVP_EncryptInit_ex(ctx_enc, EVP_aes_128_cbc(), NULL, aes_key, iv)) handle_openssl_error();

    // Włączenie dopełniania PKCS (domyślnie włączone, ale lepiej jawnie)
    if (!EVP_CIPHER_CTX_set_padding(ctx_enc, 1)) handle_openssl_error();

    // Szyfrowanie danych (Update)
    if (!EVP_EncryptUpdate(ctx_enc, ciphertext, &len_update, (unsigned char*)plaintext, plaintext_len)) handle_openssl_error();
    ciphertext_len = len_update;

    // Finalizacja szyfrowania (dodanie dopełnienia)
    if (!EVP_EncryptFinal_ex(ctx_enc, ciphertext + len_update, &len_final)) handle_openssl_error();
    ciphertext_len += len_final;

    EVP_CIPHER_CTX_free(ctx_enc); // Zwolnienie kontekstu

    // --- Obliczanie HMAC ---
    if (HMAC(hmac_md, hmac_key, hmac_key_len, ciphertext, ciphertext_len, hmac_result, &hmac_len) == NULL) {
         fprintf(stderr, "HMAC calculation failed\n");
         handle_openssl_error();
    }

    // Sprawdzenie, czy wynik zmieści się w buforze
    total_payload_len = ciphertext_len + hmac_len;
    if (total_payload_len > MAX_BUFF_SIZE) {
        fprintf(stderr, "Error: Encrypted data + HMAC is too large for buffer (%d > %d)\n", total_payload_len, MAX_BUFF_SIZE);
        exit(EXIT_FAILURE);
    }

    // --- Przygotowanie payloadu ---
    memcpy(send_buffer, ciphertext, ciphertext_len);
    memcpy(send_buffer + ciphertext_len, hmac_result, hmac_len);

    // --- Komunikacja sieciowa ---
    sockfd = socket(PF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("socket()");
        exit(EXIT_FAILURE);
    }

    memset(&remote_addr, 0, sizeof(remote_addr));
    remote_addr.sin_family = AF_INET;
    retval = inet_pton(AF_INET, argv[1], &remote_addr.sin_addr);
    if (retval <= 0) {
        if (retval == 0) fprintf(stderr, "inet_pton(): invalid network address!\n");
        else perror("inet_pton()");
        exit(EXIT_FAILURE);
    }
    remote_addr.sin_port = htons(atoi(argv[2]));
    addr_len = sizeof(remote_addr);

    fprintf(stdout, "Sending encrypted message with HMAC to %s:%s...\n", argv[1], argv[2]);

    retval = sendto(sockfd, send_buffer, total_payload_len, 0,
                    (struct sockaddr*)&remote_addr, addr_len);

    if (retval == -1) {
        perror("sendto()");
        exit(EXIT_FAILURE);
    }

    close(sockfd);
    ERR_free_strings(); // Cleanup OpenSSL
    // EVP_cleanup(); // Jeśli używano OpenSSL_add_all_digests()

    exit(EXIT_SUCCESS);
}