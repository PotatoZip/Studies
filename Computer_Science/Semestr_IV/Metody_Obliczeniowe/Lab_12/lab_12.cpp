#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>

#define dx 1e-2
#define N 15
#define A -1
#define B 1
#define Pi 3.14159265359
double x[N];

double functionValue(double x) { return 1.0 / (1.0 + 10.0 * x * x * x * x * x * x); }
 // pętla licząca kolejne wartości interpolacji na węzłach równoodległych 
void interpolation() { for (int i = 0; i < N; ++i) { x[i] = A + i * ((B - A) / (N - 1.0)); } }


 // pętla licząca kolejne wartości interpolacji na węzłach Czebyszewa 
void czebyszewValue() {
    double tmp;
    for (int i = 0; i < N; ++i) {
        tmp = cos(((2.0 * i + 1.0) / (2.0 * N + 2.0)) * Pi);
        x[i] = (B + A) / 2.0 + ((B - A) / 2.0) * tmp;
    }
}

// baza Newtona do kontrukcji wielomianów interpolacyjnych
void newton(const std::string& filename) { 
    std::cout << filename << std::endl;
    double c[N][N];
    for (int i = 0; i < N; ++i) { c[i][0] = functionValue(x[i]); }

    for (int i = 1; i < N; ++i) {
        for (int j = 0; j < N - i; ++j) {
            c[j][i] = (c[j + 1][i - 1] - c[j][i - 1]) / (x[i + j] - x[j]);
        }
    }

    std::fstream file;
    file.open( std::string ("results_") + filename + (".txt"), std::fstream::out);
    double value;
    for (double ix = A; ix <= B; ix += dx) {
        value = c[0][N - 1];
        for (int i = N - 1; i > 0; --i) {
            value *= (ix - x[i - 1]);
            value += c[0][i - 1];
        }
        file << ix << "\t" << value << std::endl;
    }
    file.close();
}

// funkcja zapisująca dokładne wyniki do pliku 
void saveToFile() { 
    std::cout << "dokladne" << std::endl;
    std::fstream result_Dokladne;
    result_Dokladne.open( "results_dokladne.txt", std::fstream::out);
    result_Dokladne << std::scientific;
    for (double ix = A; ix <= B; ix += dx) { result_Dokladne << ix << "\t" << functionValue(ix) << std::endl; }
    result_Dokladne.close();
}

int main() {
    interpolation();
    newton("rownoodlegle");

    czebyszewValue();
    newton("czebyszew");
    
    saveToFile();

    return 0;
}
