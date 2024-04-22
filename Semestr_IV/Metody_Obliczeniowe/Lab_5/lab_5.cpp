#include <iostream>
#include <math.h>
#include <iomanip>

#define N 4

double matrixA[N][N] = {
    1.0, -20.0, 30.0, -4.0,
    2.0, -40.0, -6.0, 50.0,
    9.0, -180.0, 11.0, -12.0,
    -16.0, 15.0, -140.0, 13.0
};

double vectorB[N] = {35.0, 104.0, -366.0, -354.0};
double indx[N] = {0, 1, 2, 3};

double matrixL[N][N];
double x[N];
double y[N];

void printMatrix(double matrix[N][N]);
void printVector(double vec[N]);
void gauss(double matrixA[N][N], double matrixL[N][N], int i);
void swap(double matrixA[N][N], double matrixL[N][N], double tmpVector[N], int i);
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
    std::cout << "Macierz A:" << std::endl;
    printMatrix(matrixA);
    std::cout << "Wektor B:" << std::endl;
    printVector(vectorB);

    for (int i = 0; i < N; i++) {
        if (matrixA[i][i] == 0) {
            std::cout << "Wykryto 0 w macierzy A!" << std::endl;
            printMatrix(matrixA);
            swap(matrixA, matrixL, indx, i);
        }
        gauss(matrixA, matrixL, i);
    }
}

void solve() {

    std::cout << "Po eliminacji Gaussa\n" << std::endl;
    std::cout << "Macierz A:" << std::endl;
    printMatrix(matrixA);
    std::cout << "Wektor B:" << std::endl;
    printVector(vectorB);

    //

    int tmp;
    double tmpVector[N];

    for (int i = 0; i < N; i++) {
        tmpVector[i] = vectorB[i];
    }
    for (int i = 0; i < N; i++) {
        tmp = indx[i];
        vectorB[i] = tmpVector[tmp];
    }

    std::cout << "Wektor B po zmianie kolejnosci:" << std::endl;
    printVector(vectorB);

    //

    for (int i = 0; i < N; i++) {
        for (size_t i = 0; i < N; i++) {
            y[i] = vectorB[i];
        }

        for (int k = 1; k < N; ++k) {
            for (int i = k; i < N; ++i) {
                y[i] -= y[k - 1] * matrixL[i][k - 1];
            }
        }
    }

    //

    for (int i = N - 1; i >= 0; i--) {
        x[N - 1] = y[N - 1] / matrixA[N - 1][N - 1];
        double suma;
        for (int i = N - 2; i >= 0; i--) {
            suma = 0.0;
            for (int k = N - 1; k > i; k--) {
                suma = suma + x[k] * matrixA[i][k];
            }
            x[i] = (y[i] - suma) / matrixA[i][i];
        }
    }

    std::cout << "Wektor Y:" << std::endl;
    printVector(y);
    std::cout << "Wektor X:" << std::endl;
    printVector(x);
}

void gauss(double matrixA[N][N], double matrixL[N][N], int i) {
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

void swap(double matrixA[N][N], double matrixL[N][N], double vecHelp[N], int i) {
    double tmpA[N];
    int tmpVector;
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

    tmpVector = vecHelp[i];
    vecHelp[i] = vecHelp[maxIdx];
    vecHelp[maxIdx] = tmpVector;

    for (int j = 0; j < i; j++) {
        tmpA[j] = matrixL[maxIdx][j];
        matrixL[maxIdx][j] = matrixL[i][j];
        matrixL[i][j] = tmpA[j];
    }
}

void printMatrix(double matrix[N][N]) {
    std::cout << "==========================" << std::endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << "\n";
    }
    std::cout << "==========================" << std::endl;
}

void printVector(double vec[N]) {
    std::cout << "==========================" << std::endl;
    for (int i = 0; i < N; i++) {
        std::cout << vec[i] << "\t";
    }
    std::cout << "\n==========================" << std::endl;
}