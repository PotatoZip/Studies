#include <stdio.h>

int main() {
	int cols, rows;
	printf("Enter count of columns and rows\n");
	scanf("%d %d", &cols, &rows);
	int arr_A[rows][cols], arr_B[cols][rows], arr_AB[rows][rows];
	printf("Start entering matrix A of %dx%d size\n", rows, cols);
	for(int i = 0; i < rows; i++) {
		for(int j = 0; j < cols; j++) {
			scanf("%d", &arr_A[i][j]);
		}
	}
	printf("Do it again for matrix B of %dx%d size\n", cols, rows);
	for(int i = 0; i < cols; i++) {
		for(int j = 0; j < rows; j++) {
			scanf("%d", &arr_B[i][j]);
		}
	}
	printf("Matrix A * B:\n");
	for(int i = 0; i < rows; i++) {
		for(int j = 0; j < rows; j++) {
			for(int k = 0; k < cols; k++) {
				arr_AB[i][j] += arr_A[i][k] * arr_B[k][j];
			}
			printf("%d ", arr_AB[i][j]);
		}
		printf("\n");
	}
	return 0;
}
