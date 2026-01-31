#include <stdio.h>

int euclid_algorithm(int a, int b){
	while(b > 0){
		int c = a%b;
		a = b;
		b = c;
	}
	return a;
}

int main(){
	int a,b;
	printf("Enter two values\n");
	scanf("%d %d", &a,&b);
	printf("The greatest common divisor of %d and %d is: %d\n", a, b, euclid_algorithm(a,b));
}
