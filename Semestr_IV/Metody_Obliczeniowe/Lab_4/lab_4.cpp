#include <iostream>
#include <math.h>
#include <vector>
#include <cfloat>

const double TOLX = 1e-10;
const double TOLF = 1e-10;
int iterMax = 100;
double est1,est2,est3,estMax,residMax;

double function1(double x, double y, double z);
double function2(double x, double y);
double function3(double x, double y);
double result1(double x, double y);
double result2(double y);
double result3(double z);
double maxValue(double a, double b, double c);

int main() {
    int n = 0;
    double xn[3] = {10.0, 20.0, 40.0};
    double xn1[3] = {0.0, 0.0, 0.0};
    double resid[3] = {0.0, 0.0, 0.0};
    
    do {
        xn1[0] = xn[0] - result1(xn[0], xn[1]);
        xn1[1] = xn[1] - result2(xn[1]);
        xn1[2] = xn[2] - result3(xn[2]);
        est1 = fabs(xn1[0] - xn[0]);
        est2 = fabs(xn1[1] - xn[1]);
        est3 = fabs(xn1[2] - xn[2]);
        resid[0] = fabs(function1(xn1[0], xn1[1], xn1[2]));
        resid[1] = fabs(function2(xn1[0], xn1[1]));
        resid[2] = fabs(function3(xn1[0], xn1[1]));
        xn[0] = xn1[0];
        xn[1] = xn1[1];
        xn[2] = xn1[2];
        estMax = maxValue(est1, est2, est3);
        residMax = maxValue(resid[0], resid[1], resid[2]);
        printf("iteracja[%d] | xn[0]: %.4e | xn[1]: %.4e | xn[2]: %.4e | estMax: %.4e | residuumMax: %.4e \n",n,xn[0],xn[1],xn[2], estMax, residMax);

        if (n >= iterMax) {
            std::cout << "Osiagnieto max iteracji (ustawione na:" << iterMax << ")\n" << std::endl;
        }
        if(fabs(estMax) <= TOLX) {
            std::cout << "Estymator (Max) przyjal minimala wartosc (mniejsze od epsilona)\n" << std::endl;
        }
        if(fabs(residMax) <= TOLF) {
            std::cout << "Osiagnieto maksymalne przyblizenie (residuum)\n" << std::endl;
        }
        n++;
    } while (n <= iterMax && (fabs(estMax) >= TOLX && fabs(residMax) >= TOLF));

    std::cout << "=================\n      Wynik\n=================\n" << std::endl;
    std::cout << "xn[0]: " << xn[0] << "\t" << "xn[1]: " << xn[1] << "\t" << "xn[3]: " << xn[2] << std::endl;

    return 0;
}

double function1(double x, double y, double z) { return x*x + y*y + z*z - 2.0; }
double function2(double x, double y) { return x*x + y*y- 1; }
double function3(double x, double y) { return x*x - y; }
double result1(double x, double y) { return (x*x - y*y + 2.0*x*x*y - 1.0)/(2.0*x + 4.0*x*y); }
double result2(double y) { return (y*y + y - 1.0)/(1.0 + 2.0*y); }
double result3(double z) { return (z*z - 1.0)/(2.0*z); }
double maxValue(double a, double b, double c) {
    if ((a >= b) && (a >= c)) {
        return a;
    } else if ((b >= a) && (b >= c)) {
        return b;
    } else {
        return c;
    }
}