#include <stdio.h>

int main() {
	int arr[10];
	printf("Enter 10 values\n");
	for(int i = 0; i < 10; i++)
		scanf("%d", &arr[i]);
	for(int j = 0; j < 10 - 1; j++){
		for(int k = 0; k < 10 - 1 - j; k++) {
			if(arr[k] > arr[k + 1]) {
				int temp = arr[k];
				arr[k] = arr[k+1];
				arr[k+1] = temp;
			}
		}
	}
	printf("Sorted values:\n");
	for(int l = 0; l < 10; l++)
		printf("%d\n", arr[l]);
	return 0;
}
