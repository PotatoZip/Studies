#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/errno.h>
#include <fcntl.h>

#define N 5 // Liczba semaforow

int main(int argc, char *argv[]) {
    key_t kluczs,kluczm,kluczStan; //klucz do semaforow i pam. dzielonej
    int semID;           //identyfikator zestawu semaforow
    int shmID;           //inentyfikator pamieci dzielonej
    //int idStan;
    //int shmidStan;
    int semidFork;
    char bufor[3];       //bufor
    int *widelec;        //tablica widelcow pamiec dzielona
    //int *stany;
    
    if ( (kluczs = ftok(".", 'A')) == -1 ) {
        printf("Blad ftok (main)\n"); exit(1);
    }
    
    //Tworzenie zestawu semaforow
    if ((semID = semget(kluczs, N + 1, IPC_CREAT | IPC_EXCL | 0666)) == -1) {
        perror("Blad semget:");
        exit(1);
    }

    //Inicjalizacja semaforow
    for(int i = 0; i < N; i++) {
        if ( semctl(semID, i, SETVAL, 1) == -1 ) {
            perror("Blad semctl (inicjalizujSemafor): ");
            exit(1);
        }
    }

    //klucz do pamieci dzielonej
    kluczm=ftok(".",'B');
    //kluczStan=ftok(".","C");
    
    //tworzenie pamieci dzielonej
    shmID=shmget(kluczm,N*sizeof(int),IPC_CREAT|IPC_EXCL|0666);
    //idStan=shmget(kluczStan,N*sizeof(int),IPC_CREAT|IPC_EXCL|0666);
    if (shmID==-1) {
        printf("blad shm\n");
        exit(1);
    }

    fflush(stdout);

    //przydzielenie paamiedzi dzielonej
    widelec = shmat(shmID,NULL,0);
    //stany = shmat(idStan,NULL,0);
    semidFork = semget(kluczm, N, IPC_CREAT | 0600);
    
    for(int i = 0; i < N; i++) {
        semctl(semidFork, i, SETVAL, 1);
    }

    //Ustawienie widelcow na 0
    for (int i = 0; i < N; i++) {
        widelec[i] = 0;
    }

    // for (int i = 0; i < N; i++) {
    //     stany[i] = 0;
    // }

    //tworzenie procesow filozofow
    for (int i = 0; i < N; i++) {
        switch (fork()) {
            case -1:
                perror("Blad fork (mainp)");
                exit(2);
            case 0:
                sprintf(bufor,"%d",i); // przekazanie numeru
                execl("./filozof5","filozof5",bufor, NULL);
        }  
    }

    //czekanie na zakończenie procesow filozofow
    for (int i = 0; i < N; i++) {
         wait(NULL);
    }

    //Usuwanie semaforow
    semctl(semID, N + 1, IPC_RMID, NULL);

    //zwolnienie pamieci dzielonej
    shmctl(shmID,IPC_RMID,NULL);
    //shmctl(idStan, IPC_RMID,NULL);
    printf("MAIN: Koniec.\n");
}
