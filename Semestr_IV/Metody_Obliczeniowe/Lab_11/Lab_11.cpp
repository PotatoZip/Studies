#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <cmath>
#include "calerf.h"

#define T_MAX 2.0
#define T_MIN 0.0
#define D 1.0
#define LAMBDA_LAASONEN 1.0
#define LAMBDA_KMB 0.4
#define H 0.1
#define A 6.0*sqrt(D*T_MAX)
#define X_MIN -A
#define X_MAX A

void saveVector(std::vector<double> vector, int n, const std::string& fileName);
void saveMatrix(std::vector<std::vector<double>> matrix, int n, int m, const std::string& fileName);
double dtValue(double lambda, double h, double d);
double erfcValue(double x, double t);
void warunekPoczatkowy(std::vector<std::vector<double>> &matrix, int m);
void warunekBrzegowy(std::vector<std::vector<double>> &matrix, int n, int m);

int main() {
    return 0;
}

double erfcValue(double x, double t) { return erfc((x) / (2.0*sqrt(D*t)))/2.0; }
double dtValue(double lambda, double h, double d) { return (lambda*h*h) / d; }

void warunekPoczatkowy(std::vector<std::vector<double>> &matrix, int m) {
    double x = X_MIN;
    for (int i = 0; i < m; i++) {
        if (x < 0) {
            matrix[0][i] = 1.0;
        } else {
            matrix[0][i] = 0.0;
        }
        x += H;
    }
}

void warunekBrzegowy(std::vector<std::vector<double>> &matrix, int n, int m) {
    for (int i = 0; i < n; i++) {
        matrix[i][0] = 1.0;
        matrix[i][m - 1] = 0.0;
    }
}

void saveVector(std::vector<double> vector, int n, const std::string& fileName) {
    std::fstream file(fileName.c_str(), std::ios::out);
    if(file.is_open()) {
        for(int i = 0; i < n; i++) {
            file << vector[i] << std::endl;
        }
    }
    file.close();
}

void saveMatrix(std::vector<std::vector<double>> matrix, int n, int m, const std::string& fileName) {
    std::fstream file(fileName.c_str(), std::ios::out);
    if (file.is_open()) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                file << matrix[i][j] << " ";
            }
            file << std::endl;
        }
    }
    file.close();
}
