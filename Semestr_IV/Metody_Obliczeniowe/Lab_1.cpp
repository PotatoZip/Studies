#include <iostream>


int main() {
    float f = 1.0f;
    double d = 1.0;

    while ((f + 1.0f) != 1.0f) {
        f /= 2.0f;
    }

    while ((d + 1.0) != 1.0) {
        d /= 2.0;
    }

    float EpsilonFloat = f;
    double EpsilonDouble = d;

    std::cout << "Epsilon float: " << f << "\nEpsilon double: " << d << std::endl;

    return 0;
}