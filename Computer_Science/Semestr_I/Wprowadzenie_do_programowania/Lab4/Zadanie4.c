#include <stdio.h>
#include <math.h>

int main()
{
char ans;
double field;
printf("Which field do you want to calculate?\nCircle (c)\nTriangle (t)\nSquare (s)\n");
scanf(" %c", &ans);
if(ans == 'c')
{
	double r;
	printf("Enter radius value\n");
	scanf("%lf",&r);
	field = pow(r,2)*M_PI;
}
else if(ans == 't')
{
	double p,h;
	printf("Enter values of base length and height\n");
	scanf("%lf %lf",&p,&h);
	field = p*h/2;
}
else if(ans == 's')
{
	double a,b;
	printf("Enter lenght and wight values\n");
	scanf("%lf %lf",&a,&b);
	field = a*b;
}
else
{
	printf("Error");
}
printf("%lf",field);
return 0;
}
