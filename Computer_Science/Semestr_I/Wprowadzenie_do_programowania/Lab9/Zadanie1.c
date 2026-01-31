#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define N 3

int main() {
	double arr[N][N];
	for(int i = 0; i < N; i++) {
 		for(int j = 0; j < N; j++) {
			printf("Enter value to row: %d column: %d of your matrix\n", i+1, j+1);
			scanf("%lf", &arr[i][j]);
		}
	}
	printf("Your matrix:\n");
	for(int i = 0; i < N; i++) {
		for(int j = 0; j < N; j++) {
			printf("%lf ", arr[i][j]);
		}
		printf("\n\n");
	}
	double arr_dop[N][N];
	for(int i = 0; i < N; i++) {
		for(int j = 0; j < N; j++) {
			int id_sum = 2 + i + j;
			if(i == 0 && j == 0) {
				arr_dop[0][0] = arr[1][1] * arr[2][2] - (arr[1][2] * arr[2][1]);
			}
			else if(i == 0 && j == 1) {
				arr_dop[0][1] = arr[1][0] * arr[2][2] - (arr[1][2] * arr[2][0]);
			}
			else if(i == 0 && j == 2) {
				arr_dop[0][2] = arr[1][0] * arr[2][1] - (arr[1][1] * arr[2][0]);
			}
			else if(i == 1 && j == 0) {
				arr_dop[1][0] = arr[0][1] * arr[2][2] - (arr[0][2] * arr[2][1]);
			}
			else if(i == 1 && j == 1) {
				arr_dop[1][1] = arr[0][0] * arr[2][2] - (arr[0][2] * arr[2][0]);
			}
			else if(i == 1 && j == 2) {
				arr_dop[1][2] = arr[0][0] * arr[2][1] - (arr[0][1] * arr[2][0]);
			}
			else if(i == 2 && j == 0) {
				arr_dop[2][0] = arr[0][1] * arr[1][2] - (arr[0][2] * arr[1][1]);
			}
			else if(i == 2 && j == 1) {
				arr_dop[2][1] = arr[0][0] * arr[1][2] - (arr[0][2] * arr[1][0]);
			}
			else if(i == 2 && j == 2) {
				arr_dop[2][2] = arr[0][0] * arr[1][1] - (arr[0][1] * arr[1][0]);
			}
			arr_dop[i][j] = arr_dop[i][j] * pow(-1,id_sum);
		}
	}
	double det_arr = (arr[0][0] * arr[1][1] * arr[2][2]) + (arr[1][0] * arr[2][1] * arr[0][2]) + (arr[2][0] * arr[0][1] * arr[1][2]) - (arr[0][2] * arr[1][1] * arr[2][0]) - (arr[1][2] * arr[2][1] * arr[0][0]) - (arr[1][0] * arr[0][1] * arr[2][2]);
	if(det_arr == 0) {
		printf("Determinant of matrix equals 0\n");
		return 0;
	}
	printf("Matrix determinant%lf\n", det_arr);
	double arr_inv[N][N];
	printf("Inversed matrix:\n");
	for(int i = 0; i < N; i++) {
		for(int j = 0; j < N; j++) {
			arr_inv[i][j] = (1/det_arr)*arr_dop[j][i];
			printf("%lf ", arr_inv[i][j]);
		}
		printf("\n");
	}

	return 0;
}
