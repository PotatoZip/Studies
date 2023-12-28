#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/errno.h>
#include <unistd.h>

void signalSemafor(int semID, int number);
int alokujSemafor(key_t klucz, int number, int flagi);
int getRand(int nseed);

int main() {
   key_t klucz;
   int semID;
   int N;
   pid_t pid;

   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (C)\n");
      exit(2);
   }

   semID = alokujSemafor(klucz, N, IPC_CREAT | 0666);

   pid = getpid();

   printf("C1:%d\n", getpid());
   sleep(getRand(1));
   printf("C2:%d\n", getpid());
   sleep(getRand(2));
   signalSemafor(semID, 1);
   printf("C3:%d\n", getpid());
   sleep(getRand(4));
   signalSemafor(semID, 2);
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

int alokujSemafor(key_t klucz, int number, int flagi) {
   int semID;
   if ( (semID = semget(klucz, number, flagi)) == -1) {
      perror("Blad semget (alokujSemafor): ");
      exit(1);
   }
   return semID;
}

int getRand(int nseed) {
   int number;

   srand( nseed );
   number = rand() % 4 + 1;
   nseed = number;
   return number;
}
