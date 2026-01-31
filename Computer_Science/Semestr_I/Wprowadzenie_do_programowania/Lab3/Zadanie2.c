#include <stdio.h>

int main()
{
int a;
int b;
printf("Podaj wartosc pierwszej liczby: ");
scanf("%d",&a);
printf("Podaj wartosc drugiej liczby: ");
scanf("%d",&b);
int suma = a + b;
int roznica = a - b;
int iloczyn = a * b;
int modulo = a % b;
printf("Suma: %d\nRoznica: %d\nIloczyn: %d\nModulo: %d\n",suma,roznica,iloczyn,modulo);

return 0;
}
