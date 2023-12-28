#include <stdio.h>

int main(){
	int a[10], b[10];
	printf("Enter 10 board values\n");
	for(int i = 0; i < 10; i++)
		scanf("%d", &a[i]);
	for(int j = 0; j < 10; j++)
		b[j] = a[j];
	printf("New board values:\n");
	for(int k = 0; k < 10; k++)
		printf("%d\n", b[k]);
	return 0;
}
