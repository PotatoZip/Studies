#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <pthread.h>

pthread_t threads[100];
bool *prime;
int n;

void* eliminate_multiples(void* arg) {
    int i = *(int*)arg;
    free(arg);
    for (int j = i * i; j <= n; j += i) {
        prime[j] = false;
    }
    return NULL;
}

int main() {
    printf("Enter number:\n");
    scanf("%d", &n);
    prime = malloc((n + 1) * sizeof(bool));
    
    for (int i = 0; i <= n; i++) {
        prime[i] = true;
    }
    prime[0] = prime[1] = false;
    
    int thread_count = 0;
    for (int i = 2; i <= sqrt(n); i++) {
        if (prime[i]) {
            int* arg = malloc(sizeof(int));
            *arg = i;
            pthread_create(&threads[thread_count++], NULL, eliminate_multiples, arg);
            if (thread_count >= 100) {
                break;
            }
        }
    }
    
    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }
    
    for (int i = 2; i <= n; i++) {
        if (prime[i]) {
            printf("%d\n", i);
        }
    }
    
    free(prime);
    return 0;
}
