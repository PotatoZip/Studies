#include <iostream>
#include <math.h>
#include <vector>

#define N 4

std::vector<std::vector<double>> matrixA = {
    {1.0, -20.0, 30.0, -4.0},
    {2.0, -40.0, -6.0, 50.0},
    {9.0, -180.0, 11.0, -12.0},
    {-16.0, 15.0, -140.0, 13.0}
};

std::vector<double> vectorB = {35.0, 104.0, -366.0, -354.0};
std::vector<int> indx = {0, 1, 2, 3};

std::vector<std::vector<double>> matrixL(N, std::vector<double>(N, 0));
std::vector<std::vector<double>> matrixU(N, std::vector<double>(N, 0));
double x[N];
double y[N];

void printMatrix(std::vector<std::vector<double>> matrix);
void printVector(std::vector<double> vec);
void gauss(std::vector<std::vector<double>> matrixA, std::vector<std::vector<double>> matrixL, int i);
void swap(std::vector<std::vector<double>> matrixA, std::vector<std::vector<double>> matrixL, std::vector<int> tmpVector, int i);
void decompositionLU();
void solve();

int main() {
    decompositionLU();
    solve();    

    return 0;
}

void decompositionLU() {
    for (int i = 0; i < N; i++) {
        matrixL[i][i] = 1.0;
    }

    for (int i = 0; i < N; i++) {
        if (matrixA[i][i] == 0) {
            swap(matrixA, matrixL, indx, i);
        }
        gauss(matrixA, matrixL, i);
    }
}

void solve() {
    int tmp;
    double tmpVector[N];

    for (int i = 0; i < N; i++) {
        tmpVector[i] = vectorB[i];
    }
    for (int i = 0; i < N; i++) {
        tmp = indx[i];
        vectorB[i] = tmpVector[tmp];
    }

    //

    for (int i = 0; i < N; i++) {
        double sum = 0.0;
        for (int j = 0; j <= i - 1; j++) {
            sum += matrixL[i][j] * y[j];
        }
        y[i] = vectorB[i] - sum;
    }

    //

    for (int i = N - 1; i >= 0; i--) {
        double sum = 0.0;
        for (int j = i+1; j < N; j++) {
            sum += matrixL[i][j] * x[j];
        }
        x[i] = (y[i] - sum) / matrixA[i][i];
    }

    printMatrix(matrixA);
    printMatrix(matrixL);
    printMatrix(matrixU);
}

void gauss(std::vector<std::vector<double>> matrixA, std::vector<std::vector<double>> matrixL, int i) {
    double tmp;
    for (int j = i + 1; j < N; j++) {
        if (matrixA[j][i] == 0.0) {
            matrixL[j][i] = 0.0;
        } else {
            tmp = matrixA[j][i] / matrixA[i][i];
            for (int z = i; z < N; z++) {
                matrixA[j][z] = matrixA[j][z] - (tmp*matrixA[i][z]);
            }
            matrixL[j][i] = tmp;
        }
    }
}

void swap(std::vector<std::vector<double>> matrixA, std::vector<std::vector<double>> matrixL, std::vector<int> tmpVector, int i) {
    std::vector<double> tmpA;
    int vec;
    int maxIdx;
    double maxInRow = 0.0;

    for (int j = i + 1; j < N; j++) {
        if (abs(matrixA[j][i]) > maxInRow) {
            maxIdx = j;
            maxInRow = abs(matrixA[j][i]);
        }
    }

    for (int j = 0; j < N; j++) {
        tmpA[j] = matrixA[maxIdx][j];
        matrixA[maxIdx][j] = matrixA[i][j];
        matrixA[i][j] = tmpA[j];
    }

    vec = tmpVector[i];
    tmpVector[i] = tmpVector[maxIdx];
    tmpVector[maxIdx] = vec;

    for (int j = 0; j < i; j++) {
        tmpA[j] = matrixL[maxIdx][j];
        matrixL[maxIdx][j] = matrixL[i][j];
        matrixL[i][j] = tmpA[j];
    }
}

void printMatrix(std::vector<std::vector<double>> matrix) {
    std::cout << "==========================" << std::endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << "\n";
    }
    std::cout << "==========================" << std::endl;
}

void printVector(std::vector<double> vec) {
    std::cout << "=============" << std::endl;
    for (int i = 0; i < N; i++) {
        std::cout << vec[i] << " ";
    }
    std::cout << "=============" << std::endl;
}