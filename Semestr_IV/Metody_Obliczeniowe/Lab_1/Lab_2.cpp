#include <iostream>
#include <cmath>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>

using namespace std;

const double epsilon = 2.22045e-16;

double expFunction(double x) {
    return (1.0 - exp(-x))/x;
}

double bladLogarytmu(double x, double y) {
    return log10(abs(x - y)/y);
}

double taylorFunction(double x, double res) { 
    double result = 0.0;
    double taylor = 1.0;
    int n = 2;
    while (abs(result - res) > epsilon) { 
        result += taylor;
        taylor *= -x / n;
        n++;
        if (taylor == 0) {
			break;
		}
    }
    return result;
}

int main() {
    std::ifstream file;
    std::ofstream wynikiExp;
    std::ofstream wynikiTaylor;
    std::ofstream wynikiFinal;
    file.open("dane.txt", std::ios::in);
    wynikiExp.open("wyniki_exp.txt", std::ios::out);
    wynikiTaylor.open("wyniki_taylor.txt", std::ios::out);
    wynikiFinal.open("wyniki_final.txt", std::ios::out);
    std::string line;

    while(file.good()) {
        getline(file, line);
        std::istringstream stream(line);
        double logValue, xValue, functionValue;
        std:stream >> logValue >> xValue >> functionValue;
        double error = bladLogarytmu(expFunction(xValue), functionValue);

        wynikiExp << std::scientific << std::setprecision(20) << logValue << " " << std::scientific << std::setprecision(20) << error << std::endl;
        wynikiTaylor << std::scientific << std::setprecision(20) << logValue << " " << std::scientific << std::setprecision(20) << bladLogarytmu(taylorFunction(xValue, functionValue), functionValue) << std::endl;

        if (xValue < 0.1) {
			wynikiFinal << std::scientific << std::setprecision(20) << logValue << " " << std::scientific << std::setprecision(20) << bladLogarytmu(taylorFunction(xValue, functionValue),functionValue) << std::endl;
		}
        else {
            wynikiFinal << std::scientific << std::setprecision(20) << logValue << " " << std::scientific << std::setprecision(20) << bladLogarytmu(expFunction(xValue), functionValue) << std::endl;
        }

    }

    file.close();
    wynikiExp.close();
    wynikiTaylor.close();
    wynikiFinal.close();

    return 0;
}