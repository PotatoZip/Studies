#include <stdio.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <time.h>
#include <sys/sem.h>

#define MAX 10
#define MAX2 12
#define PELNY 2
#define PUSTY 1
#define odczyt pam[MAX]
#define zapis pam[MAX+1]

void signalSemafor(int semID, int number);      // funkcja podnoszenia semaforu
int waitSemafor(int semID, int number, int flags);    // funkcja opuszczania semaforu


struct bufor {
	int mtype;
	int mvalue;
};

int *pam;

int main() {
   key_t klucz, kluczm,kluczs;
   int msgID;
   int shmID, semID;
   time_t czas;
   struct bufor komunikat, sendInfo;

   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (A)\n");
      exit(2);
   }

   msgID=msgget(klucz, IPC_CREAT | 0666);
   
   if (msgID==-1) {
      printf("blad klejki komunikatow\n");
      exit(1);
   }

   kluczm= ftok(".", 'B');
   kluczs= ftok(".", 'C');
   shmID=shmget(kluczm, MAX2*sizeof(int),IPC_CREAT|0666);
   pam=(int*)shmat(shmID, NULL, 0);

   //odbiokomunikatu
   if (msgrcv(msgID,&komunikat,sizeof(int),PUSTY,0)==-1) {
      perror("blad odbioru komunikatu\n");
      exit(1);
   }

   semID=semget(kluczs,1,IPC_CREAT|0666);

   pam[komunikat.mvalue] = 0;

   sleep(getpid()%10);
   struct sembuf operacje;
   // w sekcji krytycznej  zapis PID-u (getpid()) do puli buforow pod indeks zapis
   // wypisanie informacji na ekranie
   // modyfikacja indeksu do zapisu
   // wyslanie odpowiedniego komunikatu

   waitSemafor(semID, 0, SEM_UNDO);
   int writeIndexSharedMem = pam[MAX + 1];
   pam[writeIndexSharedMem] = getpid();

   printf("Bufor: %d, zawartosc: %d\n", writeIndexSharedMem, getpid());

   pam[MAX+1] = (pam[MAX + 1] + 1 ) % MAX;

   signalSemafor(semID, 0);

   sendInfo.mtype = PELNY;
   sendInfo.mvalue = 0;

   if (msgsnd(msgID, &sendInfo, sizeof(int), 0) == -1) {
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
