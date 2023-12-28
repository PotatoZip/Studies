#include <stdio.h>

int main()
{
double a,b,c;
printf("Podaj wysokosc, szerokosc i dlugosc prostopadloscianu\n");
scanf("%lf %lf %lf",&a,&b,&c);
float obj = a*b*c;
float pole = (2*a*b) + (2*a*c) + (2*b*c);
printf("Objetosc: %lf\nPole: %lf\n",obj,pole);

return 0;
}
