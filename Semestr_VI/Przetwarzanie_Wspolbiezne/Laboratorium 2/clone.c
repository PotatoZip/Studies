#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sched.h>
#include "pomiar_czasu.h"
#include "pomiar_czasu.c"

int zmienna_globalna = 0;

#define ROZMIAR_STOSU 1024*64


int funkcja_watku( void* argument ) {

  zmienna_globalna++;
  printf("%d\n", zmienna_globalna);	
  int wynik; 
  char *args[] = {"./program", NULL};
  wynik=execv("./program",args); 
   if(wynik==-1) 
     printf("Proces potomny nie wykonal programu\n");

  return 0;
}

int main()
{

  void *stos;
  pid_t pid;
  int i; 
  
  stos = malloc( ROZMIAR_STOSU );
  if (stos == 0) {
    printf("Proces nadrzędny - blad alokacji stosu\n");
    exit( 1 );
  }
  inicjuj_czas();
  for(i=0;i<1000;i++){
	
    printf("%d\n", zmienna_globalna);
    pid = clone( &funkcja_watku, (void *) stos+ROZMIAR_STOSU, 0, 0);
		 //CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_VM, 0 );
	

    waitpid(pid, NULL, __WCLONE);

  }
  drukuj_czas();
  free( stos );
}
