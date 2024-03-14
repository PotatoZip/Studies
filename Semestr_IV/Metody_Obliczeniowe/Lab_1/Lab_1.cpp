#include <iostream>

int main() {
    float epsilonFloat = 1.0f;
    double epsilonDouble = 1.0;

    int mantysaFloat = 0;
    int mantysaDouble = 0;

    while ((epsilonFloat + 1.0f) > 1.0f) {
        epsilonFloat /= 2.0f;
        mantysaFloat++;
    }
    mantysaFloat--;

    while ((epsilonDouble + 1.0) > 1.0) {
        epsilonDouble /= 2.0;
        mantysaDouble++;
    }
    mantysaDouble--;

    std::cout << "Epsilon float: " << epsilonFloat << "\nEpsilon double: " << epsilonDouble << std::endl;
    std::cout << "Mantysa dla float: " << mantysaFloat << "\nMantysa dla double: " << mantysaDouble << std::endl;
    return 0;
}