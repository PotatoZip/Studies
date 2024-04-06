#include <iostream>
#include <math.h>

double function1(double x, double y, double z);
double function2(double x, double y);
double function3(double x, double y);
double result1(double x, double y);
double result2(double y);
double result3(double z);

int main() {
    

    return 0;
}

double function1(double x, double y, double z) { return x*x + y*y + z*z - 2.0; }
double function2(double x, double y) { return x*x + y*y- 1; }
double function3(double x, double y) { return x*x - y; }
double result1(double x, double y) { return (x*x - y*y + 2.0*x*x*y - 1.0)/(2.0*x + 4.0*x*y); }
double result2(double y) { return (y*y + y - 1.0)/(1.0 + 2.0*y); }
double result3(double z) { return (z*z - 1.0)/(2.0*z); }