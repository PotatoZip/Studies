#include <stdio.h>
#include <math.h>
#include <stdbool.h>

double f1(double x, double y)
{
double y1 = log10(x) + 10;
return y1;
}

double f2(double x, double y)
{
double y2 = pow(1.5,x);\
return y2;
}

double f3(double x, double y)
{
double y3 = exp(x);
return y3;
}

int main()
{
double x,y;
printf("Enter coordinates of x and y\n");
scanf("%lf %lf",&x,&y);
if(y <= f1(x,y) && y >= f2(x,y) && y <= f3(x,y))
	printf("This point in located between this functions\n");
else
	printf("This point isn't located between this funtions\n");
return 0;
}
