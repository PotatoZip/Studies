#include <stdio.h>
#include <pthread.h>

#define ILOSC_ITERACJI 100000

int licznik = 0;

void* inkrementuj(void* arg) {
    for (int i = 0; i < ILOSC_ITERACJI; i++) {
        licznik++;
    }
    return NULL;
}

void* decrementuj(void* arg) {
    for (int i = 0; i < ILOSC_ITERACJI; i++) {
        licznik--;
    }
    return NULL;
}

int main() {
    pthread_t watek_1, watek_2;

    pthread_create(&watek_1, NULL, inkrementuj, &licznik);
    pthread_create(&watek_2, NULL, decrementuj, &licznik);

    pthread_join(watek_1, NULL);
    pthread_join(watek_2, NULL);

    printf("Wartosc po iteracjach: %d\n", licznik);

    return 0;
}