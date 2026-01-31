#include <stdio.h>
#include <time.h>
#include <unistd.h>


int main()
{


struct tm *wczas;
time_t czas;
time_t czas1;
char bufor[1024];

czas=0;
wczas=gmtime(&czas);
printf("==czas=%ld\n",czas);
strftime(bufor,1024,"%Y-%m-%d:%T",wczas);

printf("===czas 0 to: %s\n",bufor);


czas=time(&czas1);
printf("czas=%ld  czas1=%ld \n",czas,czas1); 

wczas=gmtime(&czas);
printf("==czas=%ld\n",czas);
strftime(bufor,1024,"%Y-%m-%d:%T",wczas);

printf("===czas teraz to: %s\n",bufor);







}
