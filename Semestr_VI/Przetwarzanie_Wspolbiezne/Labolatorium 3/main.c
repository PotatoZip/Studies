#include <stdio.h>
#include <pthread.h>

#define ILOSC_ITERACJI 100000

typedef struct {
    int wartosc;
    pthread_mutex_t mutex;
} Licznik;

void* inkrementuj(void* arg) {
    Licznik* licznik = (Licznik*)arg;
    for (int i = 0; i < ILOSC_ITERACJI; i++) {
        pthread_mutex_lock(&licznik->mutex);
        licznik->wartosc++;
        pthread_mutex_unlock(&licznik->mutex);
    }
    return NULL;
}

void* decrementuj(void* arg) {
    Licznik* licznik = (Licznik*)arg;
    for (int i = 0; i < ILOSC_ITERACJI; i++) {
        pthread_mutex_lock(&licznik->mutex);
        licznik->wartosc--;
        pthread_mutex_unlock(&licznik->mutex);
    }
    return NULL;
}

int main() {
    Licznik licznik;
    licznik.wartosc = 0;
    pthread_mutex_init(&licznik.mutex, NULL);
    pthread_t watek_1, watek_2;

    pthread_create(&watek_1, NULL, inkrementuj, &licznik);
    pthread_create(&watek_2, NULL, decrementuj, &licznik);

    pthread_join(watek_1, NULL);
    pthread_join(watek_2, NULL);

    printf("Wartosc po iteracjach: %d\n", licznik.wartosc);

    pthread_mutex_destroy(&licznik.mutex);

    return 0;
}