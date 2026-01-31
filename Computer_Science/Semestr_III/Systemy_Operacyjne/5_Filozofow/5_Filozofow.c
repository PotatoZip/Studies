#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/wait.h>
#include <sys/errno.h>
#include <sys/types.h>

#define P 5 // Number of philosophers
#define N 5 // Number of forks
#define Q 3 // Number of iterations

int forks[N] = {0};

void printForksState(int forks[]) {
    printf("Current state of forks: ");
    for (int i = 0; i < N; i++) {
        printf("%d ", forks[i]);
    }
    printf("\n");
}

void signalSemafor(int semID, int number) {
   struct sembuf operacje[1];
   operacje[0].sem_num = number;
   operacje[0].sem_op = 1;
   //operacje[0].sem_flg = SEM_UNDO;

   if (semop(semID, operacje, 1) == -1 ) {
      perror("Blad semop (postSemafor): ");
   }
   return;
}

int waitSemafor(int semID, int number, int flags) {
   int result;
   struct sembuf operacje[1];
   operacje[0].sem_num = number;
   operacje[0].sem_op = -1;
   operacje[0].sem_flg = 0 | flags;//SEM_UNDO;

   if ( semop(semID, operacje, 1) == -1 ) {
      //perror("Blad semop (waitSemafor)");
      return -1;
   }

}   

void philosopher(int semID, int philosopherIndex) {
    for (int i = 0; i < Q; i++) {
        printf("Philosopher %d is thinking.\n", philosopherIndex + 1);

        printf("Waiting for Semaphore: %d\n", philosopherIndex + 1);
        waitSemafor(semID, philosopherIndex, 0);
        forks[philosopherIndex] = 1;
        printf("Waiting for Semaphore: %d\n", ((philosopherIndex + 1) % N) + 1);
        waitSemafor(semID,(philosopherIndex + 1) % N, 0);
        forks[(philosopherIndex + 1) % N] = 1;

        printf("Philosopher %d is eating.\n", philosopherIndex + 1);
        printForksState(forks);

        printf("Signaling Semaphore: %d\n", philosopherIndex + 1);
        signalSemafor(semID, philosopherIndex);
        forks[philosopherIndex] = 1;
        printf("Signaling Semaphore: %d\n", ((philosopherIndex + 1) % N) + 1);
        signalSemafor(semID, (philosopherIndex+1)%N);
        forks[(philosopherIndex + 1) % N] = 1;
    }
}

int main() {
    key_t klucz;
    int semID;
    char *procesy[P] = {"A", "B", "C", "D", "E"};
    
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

    printf("Semaphores removed\n");
    fflush(stdout);

    printf("MAIN: Koniec.\n");

    return 0;
}
