#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>

#define N 5 // Ilosc semaforow
#define M 5 // Ilosc iteracji w petli

int alokujSem(key_t klucz, int number, int flagi) {
    int semID;
    if ( (semID = semget(klucz, number, flagi)) == -1) {
        perror("Blad semget (alokujSemafor): ");
        exit(1);
    }

    return semID;
}

void inicjalizujSem(int semID, int number, int val) {
    if ( semctl(semID, number, SETVAL, val) == -1 ) {
        perror("Blad semctl (inicjalizujSemafor): ");
        exit(1);
    }
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

   return 1;
}

int main(int argc, char* argv[]) {
    key_t kluczs,kluczm; //klucz do semaforow i pamieci dzielonej
    int semID;           //identyfikator zestawu semaforow
    int numer;           //numer filozofa
    int shmID;           //inentyfikator pamieci dzielonej
    char bufor[3];
    int *widelec;        //tablica widelcow

    if ( (kluczs = ftok(".", 'A')) == -1 ) {
        printf("Blad ftok (main)\n");
        exit(1);
    }

    //dostanie sie do zestawu semaforow
    semID = alokujSem(kluczs, N, IPC_CREAT | 0666);

    //tworzenie klucza
    kluczm=ftok(".",'B');

    //dostep pamieci dzielonej
    shmID=shmget(kluczm,5*sizeof(int),IPC_CREAT|0666);
    if (shmID==-1) {
        printf("blad shm\n");
        exit(1);
    }

    fflush(stdout);

    //Przylaczenie pamiedzi dzielonej
    widelec = (int*)shmat(shmID,0,0);

    //Pobiera numer filozofa
    numer= atoi(argv[1]);

    for(int i = 1; i < M + 1; i++) {

        //Myslenie
        printf("Filozof %d mysli\n", numer);
        
        //Czekanie na widelce
        waitSemafor(semID, numer, SEM_UNDO);
        waitSemafor(semID, (numer + 1) % 5, SEM_UNDO);
        
        //Podniesienie widelcow
        widelec[(numer + 1) % 5] = numer;
        widelec[numer]= numer;

        //Jedzenie
        printf("Filozof %d je\n",numer);

        //zwolnienie widelcow
        widelec[(numer + 1) % 5] = 0;
        widelec[numer] = 0;
        printf("Stan widelcow: ");

        //Sygnal dla widelcow
        signalSemafor(semID, numer);
        signalSemafor(semID, (numer + 1) % 5);
    }

    return 0;
}