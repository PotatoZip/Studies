#include <stdio.h>
#include <math.h>

int main()
{
double mi, sigma, x;
printf("Podaj wartosc Mi i Sigmy:\n");
scanf("%lf %lf",&mi,&sigma);
printf("Dla jakiego x chcesz obliczyc wartosc funkcji?\n");
scanf("%lf",&x);
float funkcja = (1/(sigma*sqrt(2*M_PI)))*exp(((-1)*pow(x-mi,2))/(2*pow(sigma,2)));
printf("Wartosc funkcji: %lf\n",funkcja);


return 0;
}
