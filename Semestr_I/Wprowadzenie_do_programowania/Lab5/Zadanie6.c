#include <stdio.h>

int fibonacci(int n){
	int x1 = 1, x2 = 1, x3;
	for(int i = 0; i < n - 2; i++){
		x3 = x1 + x2;
		x1 = x2;
		x2 = x3;
	}
	if(n == 0) return 0;
	else if(n == 1) return x1;
	else if(n == 2) return x2;
	else return x3;
}
int main(){
	int n;
	printf("Enter Fibonacci number\n");
	scanf("%d",&n);
	printf("%d\n", fibonacci(n));
	return 0;
}
