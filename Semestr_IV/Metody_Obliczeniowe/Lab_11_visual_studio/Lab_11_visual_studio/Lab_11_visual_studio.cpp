#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <cmath>
#include "calerf.h"

// Parametry do zadania
#define T_MAX 2.0
#define T_MIN 0.0
#define D 1.0
#define LAMBDA_LAASONEN 1.0
#define LAMBDA_KMB 0.4
#define H 0.1
#define A 6.0*sqrt(D*T_MAX)
#define X_MIN -A
#define X_MAX A

// Definicje funkcji
void kmb();
void laasonen();
void thomas(std::vector<std::vector<double>> a, std::vector<double> b, std::vector<double> x, int m);
void jacobie(std::vector<std::vector<double>> B, std::vector<double> b, std::vector<double> x, int m);
std::vector<std::vector<double>> klasycznaMetoda(int n, int m);
std::vector<std::vector<double>> rozwiazanieLaasonen(int n, int m, std::string funkcja);
std::vector<std::vector<double>> analitycznePodejscie(int n, int m, double dt);
std::vector<double> bledy(std::vector<std::vector<double>> wynikAnalityczny, std::vector<std::vector<double>> wynikNumeryczny, int n, int m);
std::vector<double> osX(int m);
std::vector<double> osT(double dt, int n);
std::vector<double> residuum(std::vector<std::vector<double>> a, std::vector<double> b, std::vector<double> x, int m);
double est(std::vector<double> vector1, std::vector<double> vector2, int n);
double wartoscDt(double lambda, double h, double d);
double wartoscErfc(double x, double t);
double maxVector(std::vector<double> vector, int n);
void zapiszVector(std::vector<double> vector, int n, const std::string& fileName);
void zapiszMatrix(std::vector<std::vector<double>> matrix, int n, int m, const std::string& fileName);

int main() {
    kmb();
    laasonen();
    return 0;
}

// Funkcje
void kmb() {
    double dt = wartoscDt(LAMBDA_KMB, H, D);
    int n = ((T_MAX - T_MIN) / dt);
    int m = ((X_MAX - X_MIN) / H);
    std::vector<std::vector<double>> wynikAnalityczny = analitycznePodejscie(n, m, dt);
    std::vector<std::vector<double>> wynikNumeryczny = klasycznaMetoda(n, m);
    zapiszMatrix(wynikNumeryczny, n, m, "kmb.txt");
    zapiszVector(bledy(wynikAnalityczny, wynikNumeryczny, n, m), n, "bledy_kmb.txt");
    zapiszVector(osT(dt, n), n, "os_t_kmb.txt");
    zapiszVector(osX(m), m, "os_x_kmb.txt");
}

void laasonen() {
    double dt = wartoscDt(LAMBDA_LAASONEN, H, D);
    int n = ((T_MAX - T_MIN) / dt);
    int m = ((X_MAX - X_MIN) / H);
    std::vector<std::vector<double>> wynikAnalityczny = analitycznePodejscie(n, m, dt);
    std::vector<std::vector<double>> wynikThomas = rozwiazanieLaasonen(n, m, "t");
    std::vector<std::vector<double>> wynikJacobie = rozwiazanieLaasonen(n, m, "j");
    zapiszMatrix(wynikAnalityczny, n, m, "wynik_analityczny.txt");
    zapiszMatrix(wynikThomas, n, m, "wynik_thomas.txt");
    zapiszMatrix(wynikJacobie, n, m, "wynik_jacobie.txt");
}

void jacobie(std::vector<std::vector<double>> B, std::vector<double> b, std::vector<double> x, int m) {
    double tol = 1e-8;
    std::vector<double> xTmp(m, 0.0);
    double sum;
    for (int iteracja = 0; iteracja < 100; iteracja++) {
        for (int i = 0; i < m; i++) {
            sum = 0.0;
            for (int j = 0; j < m; j++) {
                if (j != i) {
                    sum += (B[i][j] * x[j]);
                }
            }
            xTmp[i] = (-sum + b[i]) / B[i][i];
        }
        for (int i = 0; i < m; i++) {
            x[i] = xTmp[i];
        }
        if ((fabs((maxVector(residuum(B, b, x, m), m))) < tol) && (fabs((est(xTmp, x, m))) < tol)) {
            break;
        }
    }
}

void thomas(std::vector<std::vector<double>> a, std::vector<double> b, std::vector<double> x, int m) {
    std::vector<double> l(m - 1, 0.0);
    std::vector<double> d(m, 0.0);
    std::vector<double> u(m - 1, 0.0);
    d[0] = a[0][0];
    for (int i = 1; i < m - 1; i++) {
        u[i] = a[i][i + 1];
        d[i] = a[i][i];
        l[i - 1] = a[i][i - 1];
    }
    d[m - 1] = a[m - 1][m - 1];

    // Pierwszy krok Thomasa
    for (int i = 1; i < m; i++) {
        d[i] = d[i] - ((l[i - 1] / d[i - 1]) * u[i - 1]);
        b[i] = b[i] - ((l[i - 1] / d[i - 1]) * b[i - 1]);
    }

    // Drugi krok Thomasa
    x[m - 1] = b[m - 1] / d[m - 1];
    for (int i = m - 2; i >= 0; i--) {
        x[i] = (b[i] - u[i] * x[i + 1]) / d[i];
    }
}

std::vector<std::vector<double>> klasycznaMetoda(int n, int m) {
    std::vector<std::vector<double>> matrix(n, std::vector<double>(m, 0.0));
    // Warunek startowy
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
    // Warunek brzegowy
    for (int i = 0; i < n; i++) {
        matrix[i][0] = 1.0;
        matrix[i][m - 1] = 0.0;
    }
    // Metoda
    for (int i = 1; i < n; i++) {
        for (int j = 1; j < m - 1; j++) {
            matrix[i][j] = LAMBDA_KMB * (matrix[i - 1][j - 1] - 2.0 * matrix[i - 1][j] + matrix[i - 1][j + 1]) + matrix[i - 1][j];
        }
    }
    return matrix;
}

std::vector<std::vector<double>> rozwiazanieLaasonen(int n, int m, std::string funkcja) {
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

    std::vector<double> b(m, 0.0);
    std::vector<double> wynik(m, 0.0);
    for (int i = 0; i < m; i++) {
        b[i] = 0.0;
        wynik[i] = 0.0;
    }
    std::vector<std::vector<double>> a(m, std::vector<double>(m, 0.0));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            a[i][j] = 0.0;
        }
    }
    for (int k = 1; k < n; k++) {
        a[0][0] = 1.0;
        b[0] = solution[k - 1][0];
        for (int i = 1; i < m - 1; i++) {
            a[i][i + 1] = LAMBDA_LAASONEN;
            a[i][i] = -(1.0 + 2.0 * LAMBDA_LAASONEN);
            a[i][i - 1] = LAMBDA_LAASONEN;
            b[i] = -solution[k - 1][i];
        }
        b[m - 1] = 0.0;
        a[m - 1][m - 1] = 1.0;
        if (funkcja == "j") {
            jacobie(a, b, wynik, m);
        }
        else {
            thomas(a, b, wynik, m);
        }
        for (int i = 1; i < m - 1; i++) {
            solution[k][i] = wynik[i];
        }
    }
    return solution;
}

std::vector<std::vector<double>> analitycznePodejscie(int n, int m, double dt) {
    std::vector<std::vector<double>> matrix(n, std::vector<double>(m, 0.0));
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

std::vector<double> bledy(std::vector<std::vector<double>> wynikAnalityczny, std::vector<std::vector<double>> wynikNumeryczny, int n, int m) {
    std::vector<std::vector<double>> bledy(n, std::vector<double>(m, 0.0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            bledy[i][j] = fabs(wynikNumeryczny[i][j] - wynikAnalityczny[i][j]);
        }
    }
    std::vector<double> maxValue(n, 0.0);
    for (int i = 0; i < n; i++) {
        maxValue[i] = maxVector(bledy[i], m);
    }
    return maxValue;
}

std::vector<double> osX(int m) {
    std::vector<double> vector(m, 0.0);
    vector[0] = X_MIN;
    for (int i = 1; i < m; i++) {
        vector[i] = vector[i - 1] + H;
    }
    return vector;
}

std::vector<double> osT(double dt, int n) {
    std::vector<double> vector(n, 0.0);
    vector[0] = T_MIN;
    for (int i = 1; i < n; i++) {
        vector[i] = vector[i - 1] + dt;
    }
    return vector;
}

std::vector<double> residuum(std::vector<std::vector<double>> a, std::vector<double> b, std::vector<double> x, int m) {
    double sum = 0.0;
    std::vector<double> tmp(m, 0.0);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            sum += a[i][j] * x[j];
        }
        tmp[i] = sum - b[i];
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

double wartoscErfc(double x, double t) { return erfc((x) / (2.0 * sqrt(D * t))) / 2.0; }
double wartoscDt(double lambda, double h, double d) { return (lambda * h * h) / d; }

double maxVector(std::vector<double> vector, int n) {
    double max = fabs(vector[0]);
    for (int i = 1; i < n; i++) {
        if (max < fabs(vector[i])) {
            max = fabs(vector[i]);
        }
    }
    return max;
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
