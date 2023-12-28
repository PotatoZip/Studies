#include <stdio.h>

int main(){
	int a, b;
	printf("Enter dimensions lenght 'a' and 'b'\n");
	scanf("%d %d", &a, &b);
	for(int i = 0; i < a; i++){
		for(int j = 0; j < b; j++)
			printf("* ");
		printf("\n");
	}
	return 0;
}
