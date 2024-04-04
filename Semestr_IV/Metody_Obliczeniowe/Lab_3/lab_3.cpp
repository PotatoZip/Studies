#include <iostream>
#include <math.h>

const double epsilon = 2.22045e-16;
const int iterCount = 100;

void picard();
void nisection();
void newton();
void sieczna();

double function1(double x);
double function1Fi(double x);
double function1FiDx(double x);
double function2(double x);
double function2Fi(double x);
double function2FiDx(double x);


int main() {
    picard();

    return 0;
}

double function1(double x) { return sin(x/4)*sin(x/4) - x; }
double function1Fi(double x) { return sin(x/4)*sin(x/4); }
double function1FiDx(double x) {return sin(x/2)*(1/4); }
double function2(double x) { return tan(2*x) - x - 1; }
double function2Fi(double x) { return tan(2*x) - 1; }
double function2FiDx(double x) {return 2/(cos(2*x)*cos(2*x)); }

void picard() {
    int i = 0;
    double x0;
    double fiX0 = 0.5;
    
    do {
        x0 = fiX0;
        fiX0 = function2Fi(x0);
        i++;

        std::cout << i << "x0: " << x0 << "estymator:" << abs(fiX0 - x0) << "F(x0): " << function2(x0) << std::endl;
    } while ((i < iterCount) && (abs(function2(x0)) > epsilon) && (abs(fiX0 - x0) > epsilon));

    if (abs(function2FiDx(x0)) > 1) {
        std::cout << "Funkcja rozbiezna" << std::endl;
    } else {
        std::cout << "Funkcja zbiezna" << std::endl;
    }

}
