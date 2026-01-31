#include <stdio.h>

int main()
{
int x,i,sum = 0;
printf("Enter value\n");
scanf("%d",&x);
for(i = 0; i<=x; i++)sum += i;
printf("%d\n",sum);
return 0;
}
