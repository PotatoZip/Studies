#include <stdio.h>

int main()
{
int x,i,k = 0;
printf("Enter value\n");
scanf("%d",&x);
for(i = 1; i<=x; i++)
{
	if(x%i == 0)
		k += 1;
}
if(k == 2)
	printf("This value is prime\n");
else
	 printf("This value isn't prime\n");
return 0;
}
