#include <stdio.h>

int sum(int n){
	int sum = 0;
	while(n != 0){
		sum += n%10;
		n /= 10;
	}
	return sum;
}

int main(){
	int n;
	printf("Enter value\n");
	scanf("%d", &n);
	while(n >= 10){
		printf("%d ", sum(n));
		n = sum(n);
	}
	printf("\n");
	return 0;
}
