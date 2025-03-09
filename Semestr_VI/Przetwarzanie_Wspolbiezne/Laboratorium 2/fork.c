#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "pomiar_czasu.h"
#include "pomiar_czasu.c"
int zmienna_globalna=0;

int main(){
  
  int pid, wynik, i;
  inicjuj_czas();
  for(i=0;i<1000;i++){  
	printf("%d\n", zmienna_globalna);
    pid = fork(); 			
    
    if(pid==0){ 			
      
      zmienna_globalna++;
      printf("%d\n", zmienna_globalna);
      
      char *args[] = {"./program", NULL};
      wynik=execv("./program",args);
      if(wynik==-1) 
           printf("Proces potomny nie wykonal programu\n");

      exit(0);
      
    } else {					
      
      wait(NULL);
      
    }
  }
  drukuj_czas();
}
