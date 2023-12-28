#include <stdio.h>

int main()
{
int x;
printf("Enter value:\n");
scanf("%d",&x);
if(x%2 == 1)
	printf("Your value is an odd number\n");
else
	printf("Your value is an even number\n");

return 0;
}
