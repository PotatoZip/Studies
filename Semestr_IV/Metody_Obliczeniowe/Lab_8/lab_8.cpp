#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>

#define _USE_MATH_DEFINES

using namespace std;

template <typename T>
T forwardDifference(T x, T h) { return (sin(x + h) - sin(x)) / h; }
template <typename T>
T backwardDifference(T x, T h) { return (sin(x) - sin(x - h)) / h; }
template <typename T>
T centralDifference(T x, T h) { return (sin(x + h) - sin(x - h)) / (static_cast<T>(2) * h); }
template <typename T>
T forwardDifference3Point(T x, T h) { return (-static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x) + static_cast<T>(2.0) * sin(x + h) - static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x + h +h)) / h; }
template <typename T>
T backwardDifference3Point(T x, T h) { return ((static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x - h - h)) - (static_cast<T>(2.0) * sin(x - h)) + (static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x))) / h; }
template <typename T>
void calculate2(T startPoint, T centerPoint, T endPoint, T h, std::vector<T>& solution) {
    solution.push_back(log10(h));
    solution.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
    solution.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
    solution.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
    solution.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
    solution.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
    solution.push_back(log10(abs(forwardDifference3Point(startPoint, h) - cos(startPoint))));
    solution.push_back(log10(abs(forwardDifference3Point(endPoint, h) - cos(endPoint))));
}

template <typename T>
void calculate(std::string fileName, bool typ) {
    T startPoint = static_cast<T>(0.0);
    T centerPoint = static_cast<T>(M_PI / static_cast<T>(4.0));
    T endPoint = static_cast<T>(M_PI / static_cast<T>(2.0));
    T h = static_cast<T>(0.1);
    std::vector<T> solutions;
    std::vector<T> vectorP1;
    std::vector<T> vectorP2;

    for (int i = 0; i < 180; i++) {
        if(h<10e-15 && !typ) break;
        if(h<10e-7 && typ) break;
        if (i == 0) {
            vectorP1.push_back(log10(h));
            vectorP1.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
            vectorP1.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
            vectorP1.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
            vectorP1.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
            vectorP1.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
            vectorP1.push_back(log10(abs(forwardDifference3Point(startPoint, h) - cos(startPoint))));
            vectorP1.push_back(log10(abs(forwardDifference3Point(endPoint, h) - cos(endPoint))));
        }
        if (i == 6) {
            vectorP2.push_back(log10(h));
            vectorP2.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
            vectorP2.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
            vectorP2.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
            vectorP2.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
            vectorP2.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
            vectorP2.push_back(log10(abs(forwardDifference3Point(startPoint, h) - cos(startPoint))));
            vectorP2.push_back(log10(abs(forwardDifference3Point(endPoint, h) - cos(endPoint))));
        }
		
        solutions.push_back(log10(h));
        solutions.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
        solutions.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
        solutions.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
        solutions.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
        solutions.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
        solutions.push_back(log10(abs(forwardDifference3Point(startPoint, h) - cos(startPoint))));
        solutions.push_back(log10(abs(forwardDifference3Point(endPoint, h) - cos(endPoint))));

        h = h / static_cast<T>(1.2);
    }

    std::fstream file1, file2;
    file1.open(fileName+".txt", std::ios::out);
    file2.open(fileName+"_precision"+".txt", std::ios::out);
    for (int i = 0; i < solutions.size(); i++) {
        file1 << std::scientific << solutions[i] << std::endl;
    }
    for (int i = 1; i < vectorP1.size(); i++) {
         T a = (vectorP2[i] - vectorP1[i])/ (vectorP2[0] - vectorP1[0]);
		 file2 << a << std::endl;
	}

    file1.close();
    file2.close();
}

int main() {
    calculate<float>("floatSolution",1);
    calculate<double>("doubleSolution",0);

    return 0;
}