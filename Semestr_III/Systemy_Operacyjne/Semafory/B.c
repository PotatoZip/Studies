#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/errno.h>
#include <unistd.h>

int alokujSemafor(key_t klucz, int number, int flagi);
void signalSemafor(int semID, int number);
int waitSemafor(int semID, int number, int flags);
int getRand(int nseed);

int main() {
   key_t klucz;
   int semID;
   int N;
   pid_t pid;

   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (B)\n");
      exit(2);
   }

   semID = alokujSemafor(klucz, N, IPC_CREAT | 0666);

   pid = getpid();

   printf("B1:%d\n", pid);
   sleep(getRand(1));
   signalSemafor(semID,0);
   waitSemafor(semID,1,0);
   printf("B2:%d\n", pid);
   sleep(getRand(4));
   waitSemafor(semID,3,0);
   printf("B3:%d\n", pid);
   sleep(getRand(6));
}

int alokujSemafor(key_t klucz, int number, int flagi) {
   int semID;
   if ( (semID = semget(klucz, number, flagi)) == -1) {
      perror("Blad semget (alokujSemafor): ");
      exit(1);
   }
   return semID;
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

int getRand(int nseed) {
   int number;

   srand( nseed );
   number = rand() % 4 + 1;
   nseed = number;
   return number;
}
