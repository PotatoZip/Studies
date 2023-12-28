#include <stdio.h>

void swap(int *a, int *b) {
	int temp = *a;
	*a = *b;
	*b = temp;
}

int main() {
	int arr[10];
	printf("Enter 10 values\n");
	for(int i = 0; i < 10; i++)
		scanf("%d", &arr[i]);
	for(int i = 0; i < 10; i++) {
		int min = arr[i], id_min = i;
		for(int j = i; j < 10; j++) {
			if(arr[j] < min) {
				min = arr[j];
				id_min = j;
			}
		}
		swap(&arr[id_min], &arr[i]);
	}
	printf("Sorted values: ");
	for(int i = 0; i < 10; i++)
		printf("%d ", arr[i]);
	printf("\n");

	return 0;
}
