#include <iostream>
#include <math.h>

const double epsilon = 2.22045e-16;
const int iterMax = 100;

void picard();
void bisection();
void newton();
void sieczna();

double function1(double x);
double function1Fi(double x);
double function1Dx(double x);
double function1FiDx(double x);
double function2(double x);
double function2Fi(double x);
double function2Dx(double x);
double function2FiDx(double x);


int main() {
    picard();
    bisection();
    newton();
    sieczna();
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

void picard() {
    std::cout << "==========================\n" << "      Metoda Picarda\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double fiX0 = 0.5;
    
    do {
        x0 = fiX0;
        fiX0 = function2Fi(x0);
        i++;

        std::cout << i << "   x0:   " << x0 << "   estymator:   " << abs(fiX0 - x0) << "   F(x0):   " << function2(x0) << std::endl;
    } while ((i < iterMax) && (abs(function2(x0)) > epsilon) && (abs(fiX0 - x0) > epsilon));

    if (abs(function2FiDx(x0)) > 1) {
        std::cout << "Funkcja jest rozbiezna" << std::endl;
    } else {
        std::cout << "Funkcja jest zbiezna" << std::endl;
    }

}

void bisection() {
    std::cout << "==========================\n" << "      Metoda Bisekcji\n" << "==========================" << std::endl;

    int i = 0;
    double a = -0.5;
    double b = 0.5;
    double c;
    double functionA, functionB, functionC;

    if (function1(a)*function1(b) >= 0) {
        std::cout << "Konce przedzialow tego samego znaku!" << std::endl;
        return;
    }
    do {
        c = (a + b) / 2.0;
        functionA = function2(a);
        functionB = function2(b);
        functionC = function2(c);
        if (((functionA > 0) && (functionC > 0)) || ((functionA < 0) && (functionC < 0))) {
            a = c;
        } 
        else if (((functionB > 0) && (functionC > 0)) || ((functionB < 0) && (functionC < 0))) {
            b = c;
        } 
        else {
            break;
        }
        i++;
        std::cout << i << "   x0:   " << c <<  "   estymator:   " << abs((b-a)/2.0) << "   F(c):   " << functionC << std::endl;
    } while ((i < iterMax) && (abs(functionC) > epsilon) && (abs((b-a)/2.0) > epsilon));
}

void newton() {
    std::cout << "==========================\n" << "      Metoda Newtona\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double fX0 = -1.0;

    do {
        x0 = fX0;
        if (function1Dx(x0) == 0) {
            std::cout << "Pochodna wynosi 0" << std::endl;
            break;
        }
        fX0 = x0 - (function1(x0)/function1Dx(x0));
        i++;
        std::cout << i << "   x0:   " << x0 << "   estymator:   " << abs(fX0-x0) << "   F(x0):   " << function1(x0) << std::endl;
    } while ((i < iterMax) && (abs(function1(x0)) > epsilon) && (abs(fX0-x0) > epsilon));
}

void sieczna() {
    std::cout << "==========================\n" << "      Metoda Siecznych\n" << "==========================" << std::endl;

    int i = 0;
    double x0;
    double x1 = -1.2;
    double x2 = 0.8;

    do {
        x0 = x1;
        x1 = x2;
        x2 = x1 - (function1(x1)/((function1(x1) - function1(x0))/(x1-x0)));
        i++;
        std::cout << i << "   x0:   " << x0 << "   estymator:   " << abs(x2-x1) << "   F(x0):   " << function1(x0) << std::endl;
    } while ((i < iterMax) && (abs(function1(x0)) > epsilon) && (abs(x2-x1) > epsilon));
}