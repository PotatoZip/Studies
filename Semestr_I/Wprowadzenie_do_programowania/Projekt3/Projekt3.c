#include <stdio.h>

//Zad. G

int main() {
	int cols, rows, sum = 0;
	printf("Enter count of columns and rows\n");
	scanf("%d %d", &cols, &rows);
	int arr[rows][cols];
	for(int i = 0; i < cols; i++) {
		for(int j = 0; j < rows; j++) {
			printf("Enter value to row: %d column: %d of your matrix\n", j+1, i+1);
			scanf("%d", &arr[j][i]);
		}
	}

	for(int i = 0; i < rows; i++) {
		for(int j = 0; j < cols; j++) {
			if(((i+1)%2 == 1) && ((j+1)%2 == 1) && ((arr[i][j])%3 == 0)) {
				sum += arr[i][j];
			}
		}
	}
	printf("Sum: %d\n", sum);
	return 0;
}
