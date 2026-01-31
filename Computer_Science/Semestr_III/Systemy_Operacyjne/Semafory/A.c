#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/errno.h>
#include <unistd.h>

//Deklaracja funkcji
int alokujSemafor(key_t klucz, int number, int flagi);
void signalSemafor(int semID, int number);
int waitSemafor(int semID, int number, int flags);
int getRand(int nseed);

int main() {
   key_t klucz;
   int semID;
   int N = 4;
   pid_t pid;

   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (A)\n");
      exit(2);
   }

   semID = alokujSemafor(klucz, N, IPC_CREAT | 0666);

   pid = getpid();

   waitSemafor(semID,0,0);
   printf("A1:%d\n", pid);
   sleep(getRand(2));
   waitSemafor(semID,2,0);
   printf("A2:%d\n", pid);
   sleep(getRand(4));
   printf("A3:%d\n", pid);
   sleep(getRand(5));
   signalSemafor(semID,3);
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

int getRand(int nseed) {
   int number;

   srand( nseed );
   number = rand() % 4 + 1;
   nseed = number;
   return number;
}
