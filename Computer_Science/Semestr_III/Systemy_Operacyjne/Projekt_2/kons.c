#include <stdio.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/sem.h>

#define MAX2 12
#define MAX 10
#define PELNY 2
#define PUSTY 1
#define zapis pam[MAX+1]
#define odczyt pam[MAX]

void signalSemafor(int semID, int number);      // funkcja podnoszenia semaforu
int waitSemafor(int semID, int number, int flags);    // funkcja opuszczania semaforu


struct bufor {
   int mtype;
   int mvalue;
};

int *pam;

int main() {
   key_t klucz, kluczm, kluczs;
   int msgID, shmID, semID;
   int i;
   struct bufor komunikat;
   sleep(1);
   printf("konsument--------------------------------\n");

   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (A)\n");
      exit(2);
   }

   msgID=msgget(klucz, IPC_CREAT | 0666);

   if (msgID==-1) {
      printf("blad klejki komunikatow\n");
      exit(1);
   }

   kluczm=ftok(".",'B');
   kluczs=ftok(".",'C');

   if ((semID=semget(kluczs,1,IPC_CREAT|0666))==-1) {
      perror("blad semafora\n");
	   exit (1);
   }

   shmID=shmget(kluczm, MAX2*sizeof(int), IPC_CREAT|0666);
   pam=(int*)shmat(shmID,NULL,0);
   // odbiorpowiedniego komunikatu
   sleep(getpid()%10);
   struct sembuf operacje;
   // w sekcji krytycznej odczyt z pamiedzielonej spod indeksu oczyt
   // uaktualnienie wskazdo odczytu (mod MAX
   // wyslanie odpowiedniego komunkat

   if (msgrcv(msgID, &komunikat, sizeof(int), PELNY, 0) == -1) { // odbieranie wiadomosci pelny i obsluga bledu
      printf("Blad przy odbieraniu wiadomoci z producenta\n");
      exit(2);
   }

   printf("Odebrano komunikat PELNY\n");

   waitSemafor(semID, 0, 0);
   int readIndex = pam[MAX];   // odczytanie wartosci z pam[10]
   int save = readIndex;   // zapisanie wartosci pod zmienna readIndex
   int pidFromSharedMem = pam[readIndex];    // odczytuje pid z pamieci wspoldzielonej 
   printf("Odczyt z bufora %d: %d\n", readIndex, pidFromSharedMem);

   pam[MAX] = (readIndex + 1) % MAX;

   signalSemafor(semID, 0);

   struct bufor sendInfo;
   sendInfo.mtype = PUSTY;
   sendInfo.mvalue = save;

   if (msgsnd(msgID, &sendInfo, sizeof(int), 0) == -1) { // wyslanie komunikatu pustego
      printf("blad wyslania komunikatu\n");
      exit(1);
   }

   return 0;
}

int waitSemafor(int semID, int number, int flags) {
   int result;
   struct sembuf operacje[1];
   operacje[0].sem_num = number;
   operacje[0].sem_op = -1;         // -1 -> wait
   operacje[0].sem_flg = 0 | flags; // SEM_UNDO;

   if (semop(semID, operacje, 1) == -1) { // wykonuje to co w sembuf struct 
      return -1;
   }

   return 1;
}

void signalSemafor(int semID, int number) {
   struct sembuf operacje[1];
   operacje[0].sem_num = number;
   operacje[0].sem_op = 1;

   if (semop(semID, operacje, 1) == -1) {
      perror("Blad semop (postSemafor): ");
   }
      
   return;
}

