#include <iostream>
#include <cmath>
#include <iomanip>
#include <fstream>
#include <algorithm>
#include <sstream>

const double p = 1.0;
const double q = 0.0;
const double r = -4.0;
const double alfa = 0.0;
const double bet = 1.0;
const double gamma = -1.0;
const double fi = 0.0;
const double psi = 1.0;
const double teta = 0.0;
const double start = 0.0;
const double stop = 1.0;

template <typename T>
T *alocation(const int size) {
    T *vector = new T[size];
    return vector;
}

template <typename T>
void deletion(T *vector) { delete[] vector; }

double solution(double x) {
    return (exp(2.0 - 2.0 * x) - 4.0 * exp(4.0 - x * 2.0) + 4.0 * exp(x * 2.0) - exp(2.0 + 2.0 * x) - x + x * exp(4.0)) / (4.0 - 4.0 * exp(4.0));
}

void thomas(const double *l, const double *d, const double *u, const double *b, double *x, int N) {
    auto *bCopy = alocation<double>(N);
    auto *dCopy = alocation<double>(N);
    bCopy[0] = b[0];
    dCopy[0] = d[0];
    for (int i = 1; i < N; i++) { dCopy[i] = d[i] - l[i - 1] * (u[i - 1] / dCopy[i - 1]); }
    for (int i = 1; i < N; i++) { bCopy[i] = b[i] - l[i - 1] * bCopy[i - 1] / dCopy[i - 1]; }
    x[N - 1] = bCopy[N - 1] / dCopy[N - 1];
    for (int i = N - 2; i >= 0; i--) { x[i] = (bCopy[i] - u[i] * x[i + 1]) / dCopy[i]; }
    deletion<double>(dCopy);
    deletion<double>(bCopy);
}

double threePointDys(double h, int N) {
    std::fstream threePoint;
    threePoint.open("three_point.txt", std::ios_base::app);
    threePoint << std::scientific;
    std::cout.precision(10);
    double *l = alocation<double>(N),
    *d = alocation<double>(N),
    *u = alocation<double>(N),
    *b = alocation<double>(N),
    *x = alocation<double>(N),
    *error = alocation<double>(N),
    xp1 = start, xp2 = start;
    u[0] = alfa / h;
    d[0] = bet - alfa / h;
    b[0] = -gamma;
    for (int i = 1; i < N - 1; i++) {
        l[i - 1] = p / (h * h) - q / (2.0 * h);
        d[i] = (-2.0 * p) / (h * h) + r;
        u[i] = p / (h * h) + q / (2.0 * h);
        b[i] = (xp1 + i * h);
    }
    l[N - 2] = -fi / h;
    d[N - 1] = -fi / h + psi;
    b[N - 1] = -teta;
    thomas(l, d, u, b, x, N);
    for (int i = 0; i < N; i++) {
        error[i] = fabs(x[i] - solution(xp2));
        xp2 += h;
    }
    if (N == 202) {
        for (int i = 0; i < N; i++) {
            threePoint << xp1 << "\t" << x[i] << std::endl;
            xp1 += h;
        }
    }
    int index = std::max_element(error, error + N) - error;
    deletion<double>(l);
    deletion<double>(d);
    deletion<double>(u);
    deletion<double>(x);
    deletion<double>(b);
    return error[index];
}

double numerowDys(double h, int N) {
    std::fstream numerow, analiticSolution;
    numerow.open("numerow.txt", std::ios_base::app);
    analiticSolution.open("analitic_solution.txt", std::ios_base::app);
    analiticSolution << std::scientific;
    numerow << std::scientific;
    double *l = alocation<double>(N),
    *d = alocation<double>(N),
    *u = alocation<double>(N),
    *b = alocation<double>(N),
    *x = alocation<double>(N),
    *error = alocation<double>(N),
    xp1 = start, xp2 = start;
    u[0] = alfa / h;
    d[0] = bet - alfa / h;
    b[0] = -gamma;
    for (int i = 1; i < N - 1; i++) {
        l[i - 1] = p / (h * h) + r / 12.0;
        d[i] = (-2.0 * p) / (h * h) + r * (10.0 / 12.0);
        u[i] = p / (h * h) + r / 12.0;
        b[i] = (xp1 + i * h - h) / 12.0 + (10.0 / 12.0) * (xp1 + i * h) + (xp1 + i * h + h) / 12.0;
    }
    l[N - 2] = -fi / h;
    d[N - 1] = -fi / h + psi;
    b[N - 1] = -teta;
    thomas(l, d, u, b, x, N);
    for (int i = 0; i < N; i++) {
        error[i] = fabs(x[i] - solution(xp2));
        xp2 += h;
    }
    if (N == 202) {
        for (int i = 0; i < N; i++) {
            numerow << xp1 << "\t" << x[i] << "\t" << std::endl;
            analiticSolution << xp1 << "\t" << solution(xp1) << std::endl;
            xp1 += h;
        }
    }
    int index = std::max_element(error, error + N) - error;
    deletion<double>(l);
    deletion<double>(d);
    deletion<double>(u);
    deletion<double>(x);
    deletion<double>(b);
    analiticSolution.close();
    numerow.close();
    return error[index];
}

int main() {
    double h, numerowError, threePointError;
    std::fstream errors;
    errors.open("errors.txt", std::fstream::out);
    errors << std::scientific;
    std::cout.precision(10);
    for (int i = 2; i < 100000; i += 100) {
        h = (stop - start) / (i - 1);
        threePointError = (threePointDys(h, i));
        numerowError = (numerowDys(h, i));
        errors << log10(h) << "\t" << log10(threePointError) << "\t" << log10(numerowError) << std::endl;
    }
    errors.close();

    return 0;
}