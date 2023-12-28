#include <stdio.h>

int main()
{
double a;
double b;
printf("Podaj wartosc pierwszej liczby: ");
scanf("%lf",&a);
printf("Podaj wartosc drugiej liczby: ");
scanf("%lf",&b);
double iloczyn = a * b;
double iloraz = a / b;
printf("Iloczyn: %lf\nIloraz: %lf\nA: %lf\nB: %lf\n",iloczyn,iloraz,a,b);

return 0;
}

