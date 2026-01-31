#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_CLIENTS 5
#define NUM_MUGS 3
#define BEER_NEEDED 2

pthread_mutex_t mugs_mutex[NUM_MUGS];
pthread_mutex_t print_mutex;

void* client(void* arg) {
    int id = *(int*)arg;
    int beer_drank = 0;

    while (beer_drank < BEER_NEEDED) {
        int mug_id = -1;
        for (int i = 0; i < NUM_MUGS; i++) {
            if (pthread_mutex_trylock(&mugs_mutex[i]) == 0) {
                mug_id = i;
                break;
            }
        }
        
        if (mug_id == -1) {
            usleep(10000);
            continue;
        }

        pthread_mutex_lock(&print_mutex);
        printf("Client number %d order beer in mug number %d.\n", id, mug_id+1);
        pthread_mutex_unlock(&print_mutex);
        
        int drink_time = rand() % 3 + 1;
        sleep(drink_time);
        beer_drank++;

        pthread_mutex_lock(&print_mutex);
        printf("Client number %d returns mug numer %d after %d sec.\n", id, mug_id+1, drink_time);
        pthread_mutex_unlock(&print_mutex);
        
        pthread_mutex_unlock(&mugs_mutex[mug_id]);
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
    pthread_mutex_init(&print_mutex, NULL);
    
    for (int i = 0; i < NUM_MUGS; i++) {
        pthread_mutex_init(&mugs_mutex[i], NULL);
    }

    for (int i = 0; i < NUM_CLIENTS; i++) {
        int* id = malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&clients[i], NULL, client, id);
    }

    for (int i = 0; i < NUM_CLIENTS; i++) {
        pthread_join(clients[i], NULL);
    }

    for (int i = 0; i < NUM_MUGS; i++) {
        pthread_mutex_destroy(&mugs_mutex[i]);
    }
    pthread_mutex_destroy(&print_mutex);
    
    printf("Pub closed.\n");
    return 0;
}
