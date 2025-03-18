#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_CLIENTS 5
#define NUM_MUGS 3
#define BEER_NEEDED 2

pthread_mutex_t mugs_mutex;
pthread_mutex_t print_mutex;
int available_mugs = NUM_MUGS;

void* client(void* arg) {
    int id = *(int*)arg;
    int beer_drank = 0;

    while (beer_drank < BEER_NEEDED) {
        pthread_mutex_lock(&mugs_mutex);
        while (available_mugs == 0) {
            pthread_mutex_unlock(&mugs_mutex);
            usleep(10000);
            pthread_mutex_lock(&mugs_mutex);
        }
        available_mugs--;
        pthread_mutex_unlock(&mugs_mutex);

        pthread_mutex_lock(&print_mutex);
        printf("Client number %d order a beer.\n", id);
        pthread_mutex_unlock(&print_mutex);
        
        int drink_time = rand() % 3 + 1;
        sleep(drink_time);
        beer_drank++;

        pthread_mutex_lock(&print_mutex);
        printf("Client number %d returned mug after %d sec.\n", id, drink_time);
        pthread_mutex_unlock(&print_mutex);
        
        pthread_mutex_lock(&mugs_mutex);
        available_mugs++;
        pthread_mutex_unlock(&mugs_mutex);
    }

    pthread_mutex_lock(&print_mutex);
    printf("Client number %d exit pub.\n", id);
    pthread_mutex_unlock(&print_mutex);

    free(arg);
    return NULL;
}

int main() {
    srand(time(NULL));
    pthread_t clients[NUM_CLIENTS];
    pthread_mutex_init(&mugs_mutex, NULL);
    pthread_mutex_init(&print_mutex, NULL);

    for (int i = 0; i < NUM_CLIENTS; i++) {
        int* id = malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&clients[i], NULL, client, id);
    }

    for (int i = 0; i < NUM_CLIENTS; i++) {
        pthread_join(clients[i], NULL);
    }

    pthread_mutex_destroy(&mugs_mutex);
    pthread_mutex_destroy(&print_mutex);
    
    printf("Pub closed.\n");
    return 0;
}
