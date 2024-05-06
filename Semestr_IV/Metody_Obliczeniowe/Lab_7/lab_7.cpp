#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

#define N 4

std::vector<std::vector<double>> matrixA = {
    {100.0, -1.0, 2.0, -3.0},
    {1.0, 200.0, -4.0, 5.0},
    {-2.0, 4.0, 300.0, -6.0},
    {3.0, -5.0, 6.0, 400.0}
}; 

std::vector<double> vectorB = {116.0, -226.0, 912.0, -1174.0};
std::vector<double> vectorX = {2.0, 2.0, 2.0, 2.0};

void jacobie();
void gaussSeidel();
void sor();
double residuum(std::vector<double> vector1, std::vector<double> vector2);
double estymator(std::vector<double> vector1, std::vector<double> vector2);
void printVector(std::vector<double> vector);
void printMatrix(std::vector<std::vector<double>> matrix);

int main() {
    //std::cout.precision(5);
    jacobie();
    for (int i = 0; i < N; i++) { vectorX[i] = 2.0; }
    gaussSeidel();
    for (int i = 0; i < N; i++) { vectorX[i] = 2.0; }
    sor();

    return 0;
}

void jacobie() {
    double tolX = 1e-12;
    double tolF = 1e-12;
    int iter = 15;
    std::vector<double> vectorU = {0.0, 0.0, 0.0, 0.0};
    std::cout << "-----------------------\n              Metoda Jacobiego\n-----------------------\n" << std::endl;
    std::cout << std::setw(10) << "Iteracja:";
    for (int i = 0; i < N; i++) {
        std::cout << std::setw(10) << "X" << i + 1;
    }
    std::cout << std::endl;
    for (int i = 0; i < N; i++) {
        double D = 1 / matrixA[i][i];
        vectorB[i] = D * vectorB[i];
        for (int j = 0; j < N; j++) {
            matrixA[i][j] = D * matrixA[i][j];
        }
    }
    for (int i = 0; i < iter; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                if (k != j) {
                    sum += matrixA[j][k] * vectorX[k];
                }
            }
            vectorU[j] = vectorB[j] - sum;
        }
        std::cout << std::setw(10) << "Iteracja: " << i;
        for (int j = 0; j < N; j++) {
            std::cout << std::setw(10) << vectorX[j];
        }
        std::cout << std::setw(20) << "Estymator: " << std::setprecision(6) << std::fixed << estymator(vectorU, vectorX);
        std::cout << std::setw(20) << "Residuum: " << std::setprecision(6) << std::fixed << residuum(vectorU, vectorB) << std::endl;
        if (estymator(vectorU, vectorX) < tolX && residuum(vectorU, vectorB) < tolF) { break; }
        for (int j = 0; j < N; j++) { vectorX[j] = vectorU[j];}
    }
}

void gaussSeidel() {
    double tolX = 1e-12;
    double tolF = 1e-12;
    int iter = 15;
    std::vector<double> vectorU = {0.0, 0.0, 0.0, 0.0};
    std::cout << "-----------------------\n              Metoda Gaussa Seidela\n-----------------------\n" << std::endl;
    std::cout << std::setw(10) << "Iteracja:";
    for (int i = 0; i < N; i++) {
        std::cout << std::setw(10) << "X" << i + 1;
    }
    std::cout << std::endl;
    for (int i = 0; i < iter; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                if (k != j) {
                    sum += matrixA[j][k] * vectorX[k];
                }
            }
            vectorX[j] = (vectorB[j] - sum) / matrixA[j][j];
        }
        std::cout << std::setw(10) << "Iteracja: " << i;
        for (int j = 0; j < N; j++) {
            std::cout << std::setw(10) << vectorX[j];
        }
        std::cout << std::setw(20) << "Estymator: " << estymator(vectorU, vectorX);
        std::cout << std::setw(20) << "Residuum: " << residuum(vectorX, vectorB) << std::endl;
        if (estymator(vectorX, vectorU) < tolX && residuum(vectorX, vectorB) < tolF) { break; }
    }
}

void sor() {
    double w = 1.0/2.0;
    double tolX = 1e-12;
    double tolF = 1e-12;
    int iter = 30;
    std::vector<double> vectorU = {0.0, 0.0, 0.0, 0.0};
    std::cout << "-----------------------\n              Metoda SOR\n-----------------------\n" << std::endl;
    std::cout << std::setw(10) << "Iteracja:";
    for (int i = 0; i < N; i++) {
        std::cout << std::setw(10) << "X" << i + 1;
    }
    std::cout << std::endl;
    for (int i = 0; i < iter; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                if (k != j) {
                    sum += matrixA[j][k] * vectorX[k];
                }
            }
            vectorX[j] = (1 - w) * vectorX[j] + w * (vectorB[j] - sum) / matrixA[j][j];
        }
        std::cout << std::setw(10) << "Iteracja: " << i;
        for (int j = 0; j < N; j++) {
            std::cout << std::setw(10) << vectorX[j];
        }
        std::cout << std::setw(20) << "Estymator: " << estymator(vectorU, vectorX);
        std::cout << std::setw(20) << "Residuum: " << residuum(vectorX, vectorB) << std::endl;
        if (estymator(vectorX, vectorU) < tolX && residuum(vectorX, vectorB) < tolF) { break; }
    }
}

double residuum(std::vector<double> vector1, std::vector<double> vector2) {
    double residuumMax = 0.0;
    for (int i = 0; i < N; i++) {
        double residuum = 0.0;
        for (int j = 0; j < N; j++) {
            residuum += matrixA[i][j] * vector1[j];
        }
        residuum -= vector2[i];
        residuumMax = std::max(fabs(residuum), residuumMax);
    }
    return residuumMax;
}

double estymator(std::vector<double> vector1, std::vector<double> vector2) {
    double estymator = 0.0;
    for (int i = 0; i < N; i++) {
        estymator = std::max(fabs(vector1[i] - vector2[i]), estymator);
    }
    return estymator;
}

void printVector(std::vector<double> vector) {
    for (int i = 0; i < N; i++) {
        std::cout << std::setw(9) << vector[i] << " " << std::endl;
    }
}

void printMatrix(std::vector<std::vector<double>> matrix) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << std::endl;
    }
}

