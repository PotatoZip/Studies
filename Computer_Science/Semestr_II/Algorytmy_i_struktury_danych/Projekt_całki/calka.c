#include <stdlib.h>
#include <stdio.h>
#include<math.h>
#include "zmiendakwiktor.c"

double f1(double x) {
    return 2.1*x*x*x*x-4.3*x*x*x-3*x+2;            
}

double f2(double x) {
    double y;
    y=2*sin(2*x)*cos(x)-cos(2.3*x)-1;
    return y;       
}


int main(int argc, char *argv[]) {
    
    printf("od=");
    scanf("%lf",&c_od);
    printf("do=");
    scanf("%lf",&c_do); 
    printf ("\n\nFunkcja 1 \n");
    printf( "wynik prostokaty - %lf\n" ,prostokaty(f1));
    printf( "wynik trapezy    - %lf\n" ,trapezy(f1));
    printf( "wynik MC   - %lf\n", mc(f1));
    printf ("\n\nFunkcja 2 \n");
    printf( "wynik prostokaty - %lf\n" ,prostokaty(f2));
    printf( "wynik trapezy    - %lf\n" ,trapezy(f2));
    printf("wynik MC   - %lf\n", mc(f2));
    printf ("\n\nFunkcja 3 \n");
	printf( "wynik prostokaty - %lf\n" ,prostokaty(f3));
    printf( "wynik trapezy    - %lf\n" ,trapezy(f3));
    printf( "wynik MC   - %lf\n", mc(f3));
    printf ("\n\nFunkcja 4 \n");
	printf( "wynik prostokaty - %lf\n" ,prostokaty(f4));
    printf( "wynik trapezy    - %lf\n" ,trapezy(f4));
    printf( "wynik MC   - %lf\n", mc(f4));
    
    system("PAUSE");
    return 0;
}
