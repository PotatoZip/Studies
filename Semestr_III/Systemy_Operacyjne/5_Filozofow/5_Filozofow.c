#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/wait.h>
#include <sys/errno.h>

#define P 5 // Number of philosophers
#define N 5 // Number of forks

void takeFork(int semID, int forkIndex) {
    struct sembuf operation = {forkIndex, -1, 0};
    semop(semID, &operation, 1);
}

void putFork(int semID, int forkIndex) {
    struct sembuf operation = {forkIndex, 1, 0};
    semop(semID, &operation, 1);
}

void philosopher(int semID, int philosopherIndex) {
    while (1) {
        printf("Philosopher %d is thinking.\n", philosopherIndex);

        // Take left fork
        takeFork(semID, philosopherIndex);
        printf("Philosopher %d picked up left fork.\n", philosopherIndex);

        // Take right fork
        takeFork(semID, (philosopherIndex + 1) % N);
        printf("Philosopher %d picked up right fork.\n", philosopherIndex);

        // Philosopher is eating
        printf("Philosopher %d is eating.\n", philosopherIndex);

        // Put down left fork
        putFork(semID, philosopherIndex);
        printf("Philosopher %d put down left fork.\n", philosopherIndex);

        // Put down right fork
        putFork(semID, (philosopherIndex + 1) % N);
        printf("Philosopher %d put down right fork.\n", philosopherIndex);
    }
}

int main() {
    key_t klucz;
    int semID;
    char *procesy[P] = {"A", "B", "C", "D", "E"};
    char sciezka[5];

    // Generate IPC key for semaphores
    if ((klucz = ftok(".", 'A')) == -1) {
        perror("Blad ftok (main)");
        exit(1);
    }

    // Allocate semaphores
    if ((semID = semget(klucz, N, IPC_CREAT | IPC_EXCL | 0666)) == -1) {
        perror("Blad semget (alokujSemafor): ");
        exit(1);
    }

    // Initialize semaphores
    for (int i = 0; i < N; i++) {
        semctl(semID, i, SETVAL, 1);
    }

    printf("Semaphores ready!\n");
    fflush(stdout);

    // Run three child processes: A, B, C, D, E using fork() and exec()
    for (int i = 0; i < P; i++) {
        switch (fork()) {
            case -1:
                perror("Blad fork (mainprog)");
                exit(2);
            case 0:
                philosopher(semID, i);
                exit(0);
        }
    }

    // Wait for child processes to finish
    for (int i = 0; i < P; i++) {
        wait(NULL);
    }

    // Remove the set of semaphores
    for (int i = 0; i < N; i++) {
      semctl(semID, 0, IPC_RMID, NULL);
    }

    printf("MAIN: Koniec.\n");

    return 0;
}
