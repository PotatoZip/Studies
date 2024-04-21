#include <iostream>
#include <math.h>
#include <iomanip>

void picard(double (*fun)(double), double (*funFi)(double), double (*funFiDx)(double));
void bisection(double (*fun)(double));
void newton(double (*fun)(double), double (*funDx)(double));
void sieczna(double (*fun)(double));

double function1(double x);
double function1Fi(double x);
double function1Dx(double x);
double function1FiDx(double x);
double function2(double x);
double function2Fi(double x);
double function2Dx(double x);
double function2FiDx(double x);


int main() {
    std::cout.precision(12);
    picard(function2, function2Fi, function2FiDx);
    bisection(function1);
    newton(function1, function1Dx);
    sieczna(function1);
    return 0;
}

double function1(double x) { return sin(x/4)*sin(x/4) - x; }
double function1Fi(double x) { return sin(x/4)*sin(x/4); }
double function1Dx(double x) {return (1/2)*sin(x/2) - 1;}
double function1FiDx(double x) {return sin(x/2)*(1/4); }
double function2(double x) { return tan(2*x) - x - 1; }
double function2Fi(double x) { return tan(2*x) - 1; }
double function2Dx(double x) { return 2/(cos(2*x)*cos(2*x)); }
double function2FiDx(double x) {return 2/(cos(2*x)*cos(2*x)); }

void picard(double (*fun)(double), double (*funFi)(double), double (*funFiDx)(double)) {
    std::cout << "==========================\n" << "      Metoda Picarda\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double fiX0 = 0.5;
    const double TOLF = 1e-10;
    const double TOLX = 1e-10;
    const int iterMax = 100;
    
    do {
        x0 = fiX0;
        fiX0 = funFi(x0);
        i++;

        std::cout << i << "   x0:   " << x0 << "   estymator:   " << fabs(fiX0 - x0) << "   Reziuduum:   " << fabs(fun(x0)) << std::endl;
    } while ((i < iterMax) && ((fabs(fun(x0)) > TOLF) && (fabs(fiX0 - x0) > TOLX)));

    if (fabs(funFiDx(x0)) > 1) {
        std::cout << "Metoda jest rozbiezna" << std::endl;
    } else {
        std::cout << "Metoda jest zbiezna" << std::endl;
    }

}

void bisection(double (*fun)(double)) {
    std::cout << "==========================\n" << "      Metoda Bisekcji\n" << "==========================" << std::endl;

    int i = 0;
    double a = -10;
    double b = 0.1;
    double c;
    double functionA, functionB, functionC;
    const double TOLF = 1e-12;
    const double TOLX = 1e-12;
    const int iterMax = 50;

    if (((fun(a) > 0) && (fun(b) > 0)) || ((fun(a) < 0) && (fun(b) < 0))) {
        std::cout << "Konce przedzialow tego samego znaku!" << std::endl;
        return;
    }
    do {
        c = (a + b) / 2.0;
        functionA = fun(a);
        functionB = fun(b);
        functionC = fun(c);
        if (((functionA > 0) && (functionC > 0)) || ((functionA < 0) && (functionC < 0))) {
            a = c;
        } 
        else if (((functionB > 0) && (functionC > 0)) || ((functionB < 0) && (functionC < 0))) {
            b = c;
        } 
        else {
            std::cout << "cos" << std::endl;
            break;
        }
        i++;
        std::cout << i << "   x0:   " << std::setw(25) << c <<  "   estymator:   " << fabs((b-a)/2.0) << "   Reziduum:   " << fabs(functionC) << std::endl;
    } while ((i < iterMax) && ((fabs(functionC) > TOLF) && (fabs((b-a)/2.0) > TOLX)));
}

void newton(double (*fun)(double), double (*funDx)(double)) {
    std::cout << "==========================\n" << "      Metoda Newtona\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double fX0 = -1.0;
    const double TOLF = 1e-10;
    const double TOLX = 1e-10;
    const int iterMax = 100;

    do {
        x0 = fX0;
        if (funDx(x0) == 0) {
            std::cout << "Pochodna wynosi 0" << std::endl;
            break;
        }
        fX0 = x0 - (fun(x0)/funDx(x0));
        i++;
        std::cout << i << "   x0:   " << x0 << "   estymator:   " << fabs(fX0-x0) << "   Reziduum:   " << fabs(fun(x0)) << std::endl;
    } while ((i < iterMax) && ((fabs(fun(x0)) > TOLF) && (fabs(fX0-x0) > TOLX)));
}

void sieczna(double (*fun)(double)) {
    std::cout << "==========================\n" << "      Metoda Siecznych\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double x1 = -1.2;
    double x2 = 0.8;
    const double TOLF = 1e-10;
    const double TOLX = 1e-10;
    const int iterMax = 100;

    do {
        x0 = x1;
        x1 = x2;
        x2 = x1 - (fun(x1)/((fun(x1) - fun(x0))/(x1-x0)));
        i++;
        std::cout << i << "   x0:   " << x0 << "   estymator:   " << fabs(x2-x1) << "   Reziduum:   " << fabs(fun(x0)) << std::endl;
    } while ((i < iterMax) && ((fabs(fun(x0)) > TOLF) && (fabs(x2-x1) > TOLX)));
}