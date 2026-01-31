#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/hmac.h> // Dodano nagłówek HMAC

int main(int argc, char **argv) {

    /* Wartosc zwracana przez funkcje: */
    // int retval; // Nie jest już potrzebna dla HMAC() w tej formie

    int i;

    /* Wiadomosc: */
    char message[64]; // Bufor na wiadomość wejściową

    /* Wynikowy kod MAC (dawniej 'digest'): */
    unsigned char mac_result[EVP_MAX_MD_SIZE]; // Bufor na wynik HMAC

    /* Rozmiar wiadomosci i kodu MAC: */
    unsigned int message_len, mac_len; // Zmieniono nazwę digest_len

    // EVP_MD_CTX *ctx; // Usunięto kontekst skrótu

    const EVP_MD* md; // Nadal potrzebne do określenia algorytmu skrótu dla HMAC

    /* Klucz dla HMAC (skopiowany z poprzednich zadań): */
    unsigned char key[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
                           0x00,0x01,0x02,0x03,0x04,0x05};
    int key_len = 16; // Długość klucza

    if (argc != 2) {
        fprintf(stderr, "Invocation: %s <DIGEST NAME for HMAC>\n", argv[0]); // Poprawiono komunikat
        exit(EXIT_FAILURE);
    }

    /* Zaladowanie tekstowych opisow bledow: */
    ERR_load_crypto_strings();

    /*
     * Zaladowanie nazw funkcji skrotu do pamieci.
     * Wymagane przez EVP_get_digestbyname():
     */
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    // Dla OpenSSL < 3.0
    OpenSSL_add_all_digests();
#else
    // W OpenSSL 3.0+ algorytmy są ładowane automatycznie przez dostawców (providers)
    // To wywołanie może nie być konieczne, ale nie powinno zaszkodzić.
    // Alternatywnie: EVP_add_digest(NULL); // Jeśli chcemy być pewni
#endif


    /* Pobranie algorytmu skrótu na podstawie nazwy z argumentu */
    md = EVP_get_digestbyname(argv[1]);
    if (!md) {
        fprintf(stderr, "Unknown message digest for HMAC: %s\n", argv[1]); // Poprawiono komunikat
        exit(EXIT_FAILURE);
    }

    /* Pobranie maksymalnie 64 znakow ze standardowego wejscia: */
    if (fgets(message, 64, stdin) == NULL) {
        fprintf(stderr, "fgets() failed!\n");
        exit(EXIT_FAILURE);
    }

    message_len = strlen(message);
    // Usunięcie potencjalnego znaku nowej linii na końcu, jeśli fgets go wczytał
    if (message_len > 0 && message[message_len - 1] == '\n') {
        message[message_len - 1] = '\0';
        message_len--;
    }


    // Usunięto alokację i inicjalizację EVP_MD_CTX

    /* Parametry bazowej funkcji skrotu (nadal mogą być interesujące): */
    fprintf(stdout, "Base Digest parameters (%s):\n", argv[1]);
    fprintf(stdout, "Block size: %d bytes\n", EVP_MD_block_size(md)); // Zmieniono na bajty dla spójności
    fprintf(stdout, "Digest size: %d bytes\n\n", EVP_MD_size(md));     // Rozmiar skrótu bazowego = rozmiar HMAC

    // Usunięto EVP_DigestInit_ex

    /* Obliczenie kodu HMAC jednym wywołaniem funkcji HMAC() */
    if (HMAC(md,           // Algorytm skrótu (np. EVP_sha256())
             key,          // Klucz
             key_len,      // Długość klucza
             (unsigned char*)message, // Wiadomość
             message_len,  // Długość wiadomości
             mac_result,   // Bufor na wynikowy kod MAC
             &mac_len      // Wskaźnik na długość wynikowego kodu MAC
            ) == NULL)
    {
        fprintf(stderr, "HMAC calculation failed\n");
        ERR_print_errors_fp(stderr);
#if OPENSSL_VERSION_NUMBER < 0x30000000L
        EVP_cleanup();
#endif
        ERR_free_strings();
        exit(EXIT_FAILURE);
    }

    // Usunięto EVP_DigestUpdate i EVP_DigestFinal_ex
    // Usunięto EVP_MD_CTX_free

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    /* Usuniecie nazw funkcji skrotu z pamieci (dla OpenSSL < 3.0). */
    EVP_cleanup();
#endif


    fprintf(stdout, "HMAC (hex): "); // Zmieniono etykietę
    for (i = 0; i < mac_len; i++) {
        fprintf(stdout, "%02x", mac_result[i]); // Użycie mac_result i mac_len
    }
    fprintf(stdout, "\n");

    /* Zwolnienie tekstowych opisow bledow: */
    ERR_free_strings();

    exit(EXIT_SUCCESS);
}