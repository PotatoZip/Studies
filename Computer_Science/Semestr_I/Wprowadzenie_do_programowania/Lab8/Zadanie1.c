#include <stdio.h>

void swap(int *a, int *b) {
	int temp = *a;
	*a = *b;
	*b = temp;
}

int main() {
	int arr[10];
	printf("Enter 10 values to array\n");
	for(int i = 0; i < 10; i++)
		scanf("%d", &arr[i]);
	for(int i = 1; i < 10; i++) {
		int val = arr[i];
		for(int j = i - 1; j >= 0; j--) { 
			if(val < arr[j])
				swap(&arr[j], &arr[j+1]);
			else
				break;
		}
	}
	printf("Sorted values: ");
	for(int i = 0; i < 10; i++)
		printf("%d ", arr[i]);
	printf("\n");
	return 0;
}
