#include <iostream>
#include <math.h>
#include <vector>

std::vector<std::vector<double>> matrixA = {
    {100.0, -1.0, 2.0, -3.0},
    {1.0, 200.0, -4.0, 5.0},
    {-2.0, 4.0, 300.0, 6.0},
    {3.0, -5.0, 6.0, 400.0}
}; 

std::vector<double> vectorB = {116.0, -226.0, 912.0, -1174.0};
std::vector<double> vecotrX = {2.0, 2.0, 2.0, 2.0};

void jacobie();
void gaussSeidel();
void sor();

int main() {
    jacobie();
    gaussSeidel();
    sor();

    return 0;
}

void jacobie() {

}

void gaussSeidel() {

}

void sor() {
    double w = 1.0/2.0;
}