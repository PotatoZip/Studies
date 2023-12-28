#include <stdio.h>

int main()
{
double a,b,wyn;
printf("Enter two values:\n");
scanf("%lf %lf",&a,&b);
if(a>b)
{
	wyn = (a/b)*100 - 100;
	printf("A is bigger by %lf %% than B\n",wyn);
}
else if(b>a)
{
	wyn = (b/a)*100 - 100;
	printf("B is bigger by %lf %% than A\n",wyn);
}
else
	printf("These are the same values");


return 0;
}
