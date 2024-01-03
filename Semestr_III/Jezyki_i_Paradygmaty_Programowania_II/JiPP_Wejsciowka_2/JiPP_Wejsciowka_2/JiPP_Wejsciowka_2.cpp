#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream stream{ "test.txt" };

    if (stream.good()) {
        std::string temp;
        while (!stream.eof()) {
            std::getline(stream, temp);
            std::cout << temp << std::endl;
        }
        stream.close();
    }



    return 0;
}
