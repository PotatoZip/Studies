#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

// ======= Matrix tools ==========
double** allocateMatrix(int rows, int cols) {
    double** matrix = malloc(rows * sizeof(double*));
    for (int i = 0; i < rows; ++i)
        matrix[i] = malloc(cols * sizeof(double));
    return matrix;
}

void freeMatrix(double** matrix, int rows) {
    for (int i = 0; i < rows; ++i)
        free(matrix[i]);
    free(matrix);
}

void fillMatrix(double** matrix, int rows, int cols) {
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            matrix[i][j] = rand() % 10;
}

// ====== Matrix Multiplication ========
void multiplyMatrices(double** A, double** B, double** C, int N, int M, int P, int mode) {
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < P; ++j)
            C[i][j] = 0;

    // Strategies
    switch (mode) {
        case 0:
            #pragma omp parallel for
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < P; ++j)
                    for (int k = 0; k < M; ++k)
                        C[i][j] += A[i][k] * B[k][j];
            break;
        case 1:
            for (int i = 0; i < N; ++i)
                #pragma omp parallel for
                for (int j = 0; j < P; ++j)
                    for (int k = 0; k < M; ++k)
                        C[i][j] += A[i][k] * B[k][j];
            break;
        case 2:
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < P; ++j) {
                    double sum = 0;
                    #pragma omp parallel for reduction(+:sum)
                    for (int k = 0; k < M; ++k)
                        sum += A[i][k] * B[k][j];
                    C[i][j] = sum;
                }
            break;
        case 3:
            #pragma omp parallel for collapse(2)
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < P; ++j)
                    for (int k = 0; k < M; ++k)
                        C[i][j] += A[i][k] * B[k][j];
            break;
        case 4:
            #pragma omp parallel for
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < P; ++j) {
                    double sum = 0;
                    #pragma omp parallel for reduction(+:sum)
                    for (int k = 0; k < M; ++k)
                        sum += A[i][k] * B[k][j];
                    C[i][j] = sum;
                }
            break;
        case 5: 
            for (int i = 0; i < N; ++i)
                #pragma omp parallel for
                for (int j = 0; j < P; ++j) {
                    double sum = 0;
                    #pragma omp parallel for reduction(+:sum)
                    for (int k = 0; k < M; ++k)
                        sum += A[i][k] * B[k][j];
                    C[i][j] = sum;
                }
            break;
        case 6:
            #pragma omp parallel for collapse(3)
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < P; ++j)
                    for (int k = 0; k < M; ++k)
                        #pragma omp atomic
                        C[i][j] += A[i][k] * B[k][j];
            break;
    }
}

int main() {
    srand(time(NULL));
    int sizes[3][3] = {
        {100, 100, 100},
        {500, 500, 500},
        {1000, 1000, 1000}
    };

    const char* strategy_names[7] = {
        "Outer loop", "Middle loop", "Inner loop",
        "Outer + Middle", "Outer + Inner",
        "Middle + Inner", "All loops"
    };

    for (int test = 0; test < 3; ++test) {
        int N = sizes[test][0];
        int M = sizes[test][1];
        int P = sizes[test][2];

        printf("\n===== Matrix size: A[%d][%d] * B[%d][%d] =====\n", N, M, M, P);

        double** A = allocateMatrix(N, M);
        double** B = allocateMatrix(M, P);
        double** C = allocateMatrix(N, P);

        fillMatrix(A, N, M);
        fillMatrix(B, M, P);

        for (int mode = 0; mode < 7; ++mode) {
            double start = omp_get_wtime();
            multiplyMatrices(A, B, C, N, M, P, mode);
            double end = omp_get_wtime();
            printf("Strategy: %-18s | Time: %.4f seconds\t | Result: ", strategy_names[mode], end - start);
            for (int i = 0; i < 4 && i < P; ++i)
                printf("%.2f ", C[0][i]);
            printf("\n");
        }

        freeMatrix(A, N);
        freeMatrix(B, M);
        freeMatrix(C, N);
    }

    return 0;
}
