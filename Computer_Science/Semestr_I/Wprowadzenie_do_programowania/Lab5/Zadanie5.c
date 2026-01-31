#include <stdio.h>

int main()
{

int x,i,sum;
printf("Enter value\n");
scanf("%d",&x);
while(x != 0){
	if(x > 0){
		sum = 1;
		for(i = 1; i<= x; i++){
			sum *= i;
		}
		printf("%d\n",sum);
	}
	else {
		printf("Your value is belove 0\n");
	}
	printf("Enter new value\n");
	scanf("%d",&x);
}
return 0;
}
