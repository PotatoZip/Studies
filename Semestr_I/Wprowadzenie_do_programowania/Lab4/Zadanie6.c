#include <stdio.h>
#include <math.h>
#include <conio.h>

double w(double a1,double a2, double b1, double b2)
{
	return a1*b2 - a2*b1;
}

double w1(double c1, double c2, double b1, double b2)
{
	return c1*b2 - c2*b1;
}

double w2(double a1, double a2, double c1, double c2)
{
	return a1*c2 - a2*c1;
}

int main()
{
double a1,a2,b1,b2,c1,c2;
printf("Enter a1 b1 c1 and a2 b2 c2 values to create two equations\n");
scanf("%lf %lf %lf %lf %lf %lf",&a1,&b1,&c1,&a2,&b2,&c2);
if(w(a1,a2,b1,b2) == 0 && w1(c1,c2,b1,b2) == 0 && w2(a1,a2,c1,c2) == 0)
	printf("Infinitely solutions\n");
else if(w(a1,a2,b1,b2) == 0 && (w1(c1,c2,b1,b2) != 0 || w2(a1,a2,c1,c2) != 0))
	printf("No solutions\n");
else
{
	double x = w1(c1,c2,b1,b2)/w(a1,a2,b1,b2), y = w2(a1,a2,c1,c2)/w(a1,a2,b1,b2);
	printf("Solution of this equations is:\nx: %lf\ny: %lf\n",x,y);
}
getch();

return 0;
}

