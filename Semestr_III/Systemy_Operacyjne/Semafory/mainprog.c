#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/errno.h>

#define P 3    // liczba procesow
#define N 4    // liczba semaforow

int main() {
   key_t klucz;
   int semID;
   char *procesy[P] = {"A", "B", "C"};
   char sciezka[5];

   //generuje  klucze IPC do semaforow '.' oznacza katalog biezacy a 'A' to identyfikator projektu
   if ( (klucz = ftok(".", 'A')) == -1 ) {
      printf("Blad ftok (main)\n");
      exit(1);
   }

   //Alokuje semafory
   if ( (semID = semget(klucz, N, IPC_CREAT | IPC_EXCL | 0666)) == -1) {
      perror("Blad semget (alokujSemafor): ");
      exit(1);
   }

   //Inicjuje mechanizmy IPC (semafory)
   for (int i = 0; i < N; i++) {
      if ( semctl(semID, i, SETVAL, 0) == -1 ) {
      perror("Blad semctl (inicjalizujSemafor): ");
      exit(1);
      }
   }

   printf("Semafory gotowe!\n");
   fflush(stdout);

   //Uruchamia trzy procesy potomne: A, B, C w oparciu o funkcje fork(), exec()
   for (int i = 0; i < P; i++) {
      switch (fork()) {
         case -1:
            perror("Blad fork (mainprog)");
            exit(2);
         case 0:
            sciezka[0] = '\0';
            strcat(sciezka, "./");
            strcat(sciezka, procesy[i]);
            execl(sciezka, procesy[i], NULL);
      }
   }

   //czeka na zakonczenie precesow
   for (int i = 0; i < P; i++) {
	wait( (int *)NULL );
   }

   //zwalnia zestaw semaforow
   for (int i = 0; i < N; i++) {
      semctl(semID, i, IPC_RMID, NULL);
   }

   printf("MAIN: Koniec.\n");
}
