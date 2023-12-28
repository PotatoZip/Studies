#include <stdio.h>

int main()
{
double a,b,wyn;
char ans;
printf("Enter two values:\n");
scanf("%lf %lf",&a,&b);
printf("Do you want to sum (+) or substract (-) this values?\n");
scanf(" %c",&ans);
if(ans == '+')
{
	wyn = a+b;
	printf("%lf\n",wyn);
}
else if(ans == '-')
{
	wyn = a-b;
	printf("%lf\n",wyn);
}
else
	printf("Error");

return 0;
}
