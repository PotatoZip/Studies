#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <cmath>
#include "calerf.h"
#include "calerf.cpp"

#define T_MAX 2.0
#define T_MIN 0.0
#define D 1.0
#define LAMBDA_LAASONEN 1.0
#define LAMBDA_KMB 0.4
#define H 0.1
#define A 6.0*sqrt(D*T_MAX)
#define X_MIN -A
#define X_MAX A

void zapiszVector(std::vector<double> vector, int n, const std::string& fileName);
void zapiszMatrix(std::vector<std::vector<double>> matrix, int n, int m, const std::string& fileName);
double wartoscDt(double lambda, double h, double d);
double wartoscErfc(double x, double t);
void warunekPoczatkowy(std::vector<std::vector<double>>& matrix, int m);
void warunekBrzegowy(std::vector<std::vector<double>>& matrix, int n, int m);
std::vector<std::vector<double>> klasycznaMetoda(int n, int m);
std::vector<std::vector<double>> analitycznePodejscie(int n, int m, double dt);
void thomas();
void jacobie();
double laasonen();
double bledy();

int main() {
    return 0;
}

double laasonen() {
    double dt = wartoscDt(LAMBDA_LAASONEN, H, D);
    int n = ((T_MAX - T_MIN) / dt);
    int m = ((X_MAX - X_MIN) / H);
    std::vector<std::vector<double>> wynikAnalityczny = analitycznePodejscie(n, m, dt);
    std::vector<std::vector<double>> wynikThomas;
    std::vector<std::vector<double>> wynikJacobie;
    zapiszMatrix(wynikAnalityczny, n, m, "wynik_analityczny.txt");
    zapiszMatrix(wynikThomas, n, m, "wynik_thomas.txt");
    zapiszMatrix(wynikJacobie, n, m, "wynik_jacobie.txt");

}

std::vector<std::vector<double>> analitycznePodejscie(int n, int m, double dt) {
    std::vector<std::vector<double>> matrix;
    double x = X_MIN;
    double t = T_MIN;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            matrix[i][j] = wartoscErfc(x, t);
            x += H;
        }
        x = X_MIN;
        t += dt;
    }
    return matrix;
}

double wartoscErfc(double x, double t) { return erfc((x) / (2.0 * sqrt(D * t))) / 2.0; }
double wartoscDt(double lambda, double h, double d) { return (lambda * h * h) / d; }

void warunekPoczatkowy(std::vector<std::vector<double>>& matrix, int m) {
    double x = X_MIN;
    for (int i = 0; i < m; i++) {
        if (x < 0) {
            matrix[0][i] = 1.0;
        }
        else {
            matrix[0][i] = 0.0;
        }
        x += H;
    }
}

void warunekBrzegowy(std::vector<std::vector<double>>& matrix, int n, int m) {
    for (int i = 0; i < n; i++) {
        matrix[i][0] = 1.0;
        matrix[i][m - 1] = 0.0;
    }
}

void zapiszVector(std::vector<double> vector, int n, const std::string& fileName) {
    std::fstream file(fileName.c_str(), std::ios::out);
    if (file.is_open()) {
        for (int i = 0; i < n; i++) {
            file << vector[i] << std::endl;
        }
    }
    file.close();
}

void zapiszMatrix(std::vector<std::vector<double>> matrix, int n, int m, const std::string& fileName) {
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
