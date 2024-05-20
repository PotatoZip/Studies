#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <cmath>
#include "calerf.h"

// Parametry do zadania
#define D 1.0
#define H 0.1
#define T_MAX 2.0
#define T_MIN 0.0
#define A 6.0*sqrt(D*T_MAX)
#define X_MIN -A
#define X_MAX A
#define LAMBDA_LAASONEN 1.0
#define LAMBDA_KMB 0.4

// Definicje funkcji
void kmb();
void laasonen();
void thomas(std::vector<std::vector<double>> matrixA, std::vector<double> vectorB, std::vector<double> vecorX, int m);
void jacobi(std::vector<std::vector<double>> matrixB, std::vector<double> vectorB, std::vector<double> vectorX, int m);
std::vector<std::vector<double>> kmbSolution(int n, int m);
std::vector<std::vector<double>> laasonenSolution(int n, int m, std::string func);
std::vector<std::vector<double>> analiticSolution(int n, int m, double dt);
std::vector<double> errors(std::vector<std::vector<double>> analitic, std::vector<std::vector<double>> numeric, int n, int m);
std::vector<double> osX(int m);
std::vector<double> osT(double dt, int n);
std::vector<double> residuum(std::vector<std::vector<double>> matrixA, std::vector<double> vectorB, std::vector<double> vectorX, int m);
double est(std::vector<double> vector1, std::vector<double> vector2, int n);
double dtValue(double lambda, double h, double d);
double erfcValue(double x, double t);
double maxVector(std::vector<double> solution, int n);
void saveVector(std::vector<double> vectorToSave, int n, const std::string& fileName);
void saveMatrix(std::vector<std::vector<double>> matrixToSave, int n, int m, const std::string& fileName);

int main() {
    kmb();
    laasonen();
    return 0;
}

// Funkcje
void kmb() {
    double dt = dtValue(LAMBDA_KMB, H, D);
    int n = ((T_MAX - T_MIN) / dt);
    int m = ((X_MAX - X_MIN) / H);
    std::vector<std::vector<double>> analiticMatrix = analiticSolution(n, m, dt);
    std::vector<std::vector<double>> numericMatrix = kmbSolution(n, m);
    saveMatrix(numericMatrix, n, m, "kmb.txt");
    saveVector(errors(analiticMatrix, numericMatrix, n, m), n, "bledy_kmb.txt");
    saveVector(osT(dt, n), n, "os_t_kmb.txt");
    saveVector(osX(m), m, "os_x_kmb.txt");
}

void laasonen() {
    double dt = dtValue(LAMBDA_LAASONEN, H, D);
    int n = ((T_MAX - T_MIN) / dt);
    int m = ((X_MAX - X_MIN) / H);
    std::vector<std::vector<double>> analiticMatrix = analiticSolution(n, m, dt);
    std::vector<std::vector<double>> thomasMatrix = laasonenSolution(n, m, "t");
    std::vector<std::vector<double>> jacobiMatrix = laasonenSolution(n, m, "j");
    saveMatrix(analiticMatrix, n, m, "wynik_analityczny.txt");
    saveMatrix(thomasMatrix, n, m, "wynik_thomas.txt");
    saveMatrix(jacobiMatrix, n, m, "wynik_jacobie.txt");
}

void jacobi(std::vector<std::vector<double>> matrixB, std::vector<double> vectorB, std::vector<double> vectorX, int m) {
    double tol = 1e-8;
    std::vector<double> xTmp(m, 0.0);
    double sum;
    for (int iter = 0; iter < 100; iter++) {
        for (int i = 0; i < m; i++) {
            sum = 0.0;
            for (int j = 0; j < m; j++) {
                if (j != i) {
                    sum += (matrixB[i][j] * vectorX[j]);
                }
            }
            xTmp[i] = (-sum + vectorB[i]) / matrixB[i][i];
        }
        for (int i = 0; i < m; i++) { vectorX[i] = xTmp[i]; }
        if ((fabs((maxVector(residuum(matrixB, vectorB, vectorX, m), m))) < tol) && (fabs((est(xTmp, vectorX, m))) < tol)) { break; }
    }
}

void thomas(std::vector<std::vector<double>> matrixA, std::vector<double> vectorB, std::vector<double> vectorX, int m) {
    std::vector<double> vectorL(m - 1, 0.0);
    std::vector<double> vectorD(m, 0.0);
    std::vector<double> vectorU(m - 1, 0.0);
    vectorD[0] = matrixA[0][0];
    for (int i = 1; i < m - 1; i++) {
        vectorU[i] = matrixA[i][i + 1];
        vectorD[i] = matrixA[i][i];
        vectorL[i - 1] = matrixA[i][i - 1];
    }
    vectorD[m - 1] = matrixA[m - 1][m - 1];

    // Pierwszy krok Thomasa
    for (int i = 1; i < m; i++) {
        vectorD[i] = vectorD[i] - ((vectorL[i - 1] / vectorD[i - 1]) * vectorU[i - 1]);
        vectorB[i] = vectorB[i] - ((vectorL[i - 1] / vectorD[i - 1]) * vectorB[i - 1]);
    }

    // Drugi krok Thomasa
    vectorX[m - 1] = vectorB[m - 1] / vectorD[m - 1];
    for (int i = m - 2; i >= 0; i--) {
        vectorX[i] = (vectorB[i] - vectorU[i] * vectorX[i + 1]) / vectorD[i];
    }
}

std::vector<std::vector<double>> kmbSolution(int n, int m) {
    std::vector<std::vector<double>> matrixRet(n, std::vector<double>(m, 0.0));
    // Warunek startowy
    double x = X_MIN;
    for (int i = 0; i < m; i++) {
        if (x < 0) {
            matrixRet[0][i] = 1.0;
        }
        else {
            matrixRet[0][i] = 0.0;
        }
        x += H;
    }
    // Warunek brzegowy
    for (int i = 0; i < n; i++) {
        matrixRet[i][0] = 1.0;
        matrixRet[i][m - 1] = 0.0;
    }
    // Metoda
    for (int i = 1; i < n; i++) {
        for (int j = 1; j < m - 1; j++) {
            matrixRet[i][j] = LAMBDA_KMB * (matrixRet[i - 1][j - 1] - 2.0 * matrixRet[i - 1][j] + matrixRet[i - 1][j + 1]) + matrixRet[i - 1][j];
        }
    }
    return matrixRet;
}

std::vector<std::vector<double>> laasonenSolution(int n, int m, std::string func) {
    std::vector<std::vector<double>> solution(n, std::vector<double>(m, 0.0));

    // Warunek poczatkowy
    double x = X_MIN;
    for (int i = 0; i < m; i++) {
        if (x < 0) {
            solution[0][i] = 1.0;
        }
        else {
            solution[0][i] = 0.0;
        }
        x += H;
    }

    // Warunek brzegowy
    for (int i = 0; i < n; i++) {
        solution[i][0] = 1.0;
        solution[i][m - 1] = 0.0;
    }

    std::vector<double> vectorB(m, 0.0);
    std::vector<double> wynik(m, 0.0);
    for (int i = 0; i < m; i++) {
        vectorB[i] = 0.0;
        wynik[i] = 0.0;
    }
    std::vector<std::vector<double>> matrixA(m, std::vector<double>(m, 0.0));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            matrixA[i][j] = 0.0;
        }
    }
    for (int k = 1; k < n; k++) {
        matrixA[0][0] = 1.0;
        vectorB[0] = solution[k - 1][0];
        for (int i = 1; i < m - 1; i++) {
            matrixA[i][i + 1] = LAMBDA_LAASONEN;
            matrixA[i][i] = -(1.0 + 2.0 * LAMBDA_LAASONEN);
            matrixA[i][i - 1] = LAMBDA_LAASONEN;
            vectorB[i] = -solution[k - 1][i];
        }
        vectorB[m - 1] = 0.0;
        matrixA[m - 1][m - 1] = 1.0;
        if (func == "j") {
            jacobi(matrixA, vectorB, wynik, m);
        }
        else {
            thomas(matrixA, vectorB, wynik, m);
        }
        for (int i = 1; i < m - 1; i++) {
            solution[k][i] = wynik[i];
        }
    }
    return solution;
}

std::vector<std::vector<double>> analiticSolution(int n, int m, double dt) {
    std::vector<std::vector<double>> matrixRet(n, std::vector<double>(m, 0.0));
    double x = X_MIN;
    double t = T_MIN;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            matrixRet[i][j] = erfcValue(x, t);
            x += H;
        }
        x = X_MIN;
        t += dt;
    }
    return matrixRet;
}

std::vector<double> errors(std::vector<std::vector<double>> analiticMatrix, std::vector<std::vector<double>> numericMatrix, int n, int m) {
    std::vector<std::vector<double>> errorsMatrix(n, std::vector<double>(m, 0.0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            errorsMatrix[i][j] = fabs(numericMatrix[i][j] - analiticMatrix[i][j]);
        }
    }
    std::vector<double> maxValue(n, 0.0);
    for (int i = 0; i < n; i++) {
        maxValue[i] = maxVector(errorsMatrix[i], m);
    }
    return maxValue;
}

std::vector<double> osX(int m) {
    std::vector<double> vectorRet(m, 0.0);
    vectorRet[0] = X_MIN;
    for (int i = 1; i < m; i++) {
        vectorRet[i] = vectorRet[i - 1] + H;
    }
    return vectorRet;
}

std::vector<double> osT(double dt, int n) {
    std::vector<double> vectorRet(n, 0.0);
    vectorRet[0] = T_MIN;
    for (int i = 1; i < n; i++) {
        vectorRet[i] = vectorRet[i - 1] + dt;
    }
    return vectorRet;
}

std::vector<double> residuum(std::vector<std::vector<double>> matrixA, std::vector<double> vectorB, std::vector<double> vectorX, int m) {
    double sum = 0.0;
    std::vector<double> tmp(m, 0.0);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            sum += matrixA[i][j] * vectorX[j];
        }
        tmp[i] = sum - vectorB[i];
        sum = 0.0;
    }
    return tmp;
}

double est(std::vector<double> vector1, std::vector<double> vector2, int n) {
    double max = abs(vector1[0] - vector2[0]);
    for (int i = 1; i < n; i++) {
        if (abs(vector1[i] - vector2[i]) > max)
            max = abs(vector1[i] - vector2[i]);
    }
    return max;
}

double erfcValue(double x, double t) { return erfc((x) / (2.0 * sqrt(D * t))) / 2.0; }
double dtValue(double lambda, double h, double d) { return (lambda * h * h) / d; }

double maxVector(std::vector<double> vector, int n) {
    double max = fabs(vector[0]);
    for (int i = 1; i < n; i++) {
        if (max < fabs(vector[i])) {
            max = fabs(vector[i]);
        }
    }
    return max;
}

void saveVector(std::vector<double> vectorToSave, int n, const std::string& fileName) {
    std::fstream file(fileName.c_str(), std::ios::out);
    if (file.is_open()) {
        for (int i = 0; i < n; i++) {
            file << vectorToSave[i] << std::endl;
        }
    }
    file.close();
}

void saveMatrix(std::vector<std::vector<double>> matrixToSave, int n, int m, const std::string& fileName) {
    std::fstream file(fileName.c_str(), std::ios::out);
    if (file.is_open()) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                file << matrixToSave[i][j] << " ";
            }
            file << std::endl;
        }
    }
    file.close();
}
