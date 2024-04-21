#include <iostream>
#include <vector>

#define N 6

std::vector<double> U = {1./2., 1./4., 1./6., 1./8., 1./10.};
std::vector<double> D = {10.0, 20.0, 30.0, 30.0, 20.0, 10.0};
std::vector<double> L = {1./3., 1./5., 1./7., 1./9., 1./11.};
std::vector<double> B = {31.0, 165./4., 917./30., 851./28., 3637./90., 332./11.};

std::vector<double> X(N);

void thomas();
void solution();

int main() {
    thomas();
    std::cout << "Przekatna po przeksztalceniu: " << std::endl;
    for (int i = 0; i < N; i++) {
        std::cout << D[i] << " ";
    }
    std::cout << std::endl;
    std::cout << std::endl;
    solution();
    for(int i = 0; i < N; i++) {
        std::cout << "X" << i << " = " << X[i] << std::endl;
    }
    
    return 0;
}

void thomas() {
    for (int i = 0; i < N; i++) {
        B[i] = B[i] - L[i - 1] * 1./D[i - 1] * B[i - 1];
    }
}

void solution() {
    X[N - 1] = B[N - 1] / D[N - 1];
    for (int i = N - 2; i >= 0; i--) {
        X[i] = 1.0 / D[i] * (B[i] - U[i] * X[i + 1]);
    } 
}