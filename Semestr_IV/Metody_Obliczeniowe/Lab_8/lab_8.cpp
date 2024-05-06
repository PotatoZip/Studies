// #include <iostream>
// #include <cmath>
// #include <fstream>
// #include <iomanip>
// #include <vector>

// #define _USE_MATH_DEFINES

// template <typename T>
// T forwardDifference(T x, T h) { return (sin(x + h) - sin(x)) / h; }
// template <typename T>
// T backwardDifference(T x, T h) { return (sin(x) - sin(x - h)) / h; }
// template <typename T>
// T centralDifference(T x, T h) { return (sin(x + h) - sin(x - h)) / (static_cast<T>(2) * h); }
// template <typename T>
// T forwardDifference3Points(T x, T h) { return (-static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x)
//         + static_cast<T>(2.0) * sin(x + h)
//         - static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x + h +h)) / h; }
// template <typename T>
// T backwardDifference3Points(T x, T h) { return ((static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x - h - h))
//         - (static_cast<T>(2.0) * sin(x - h))
//         + (static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x))) / h; }
// template <typename T>
// void oblicz_metody(T poczatek, T srodek, T koniec, T h, std::vector<T>& wyniki) {
//     wyniki.push_back(log10(h));

//     //dwupunktowe w wezlach wewnetrznych
//     wyniki.push_back(log10(abs(forwardDifference(srodek, h) - cos(srodek))));
//     wyniki.push_back(log10(abs(backwardDifference(srodek, h) - cos(srodek))));
//     wyniki.push_back(log10(abs(centralDifference(srodek, h) - cos(srodek))));
//     //dwupuntkowe w wezlach koncowych
//     wyniki.push_back(log10(abs(forwardDifference(poczatek, h) - cos(poczatek))));
//     wyniki.push_back(log10(abs(backwardDifference(koniec, h) - cos(koniec))));
//     //trzypunktowe w wezlach koncowych
//     wyniki.push_back(log10(abs(forwardDifference3Points(poczatek, h) - cos(poczatek))));
//     wyniki.push_back(log10(abs(backwardDifference3Points(koniec, h) - cos(koniec))));
// }
// template <typename T>
// void calculate(std::string fileName, bool typ) {
//     T startPoint = static_cast<T>(0.0);
//     T centerPoint = static_cast<T>(M_PI / static_cast<T>(4.0));
//     T endPoint = static_cast<T>(M_PI / static_cast<T>(2.0));
//     T h = static_cast<T>(0.1);

//     std::vector<T> solutions;
//     std::vector<T> vectorP1;
//     std::vector<T> vectorP2;

//     for (int i = 0; i < 180; i++) {
//         if (h < 10e-15 && !typ) break;
//         if (h < 10e-7 && typ) break;
//         if (i == 0) {
//             oblicz_metody(startPoint, centerPoint, endPoint, h, vectorP1);
//             // vectorP1.push_back(log10(h));
//             // vectorP1.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP1.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP1.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP1.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
//             // vectorP1.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
//             // vectorP1.push_back(log10(abs(forwardDifference3Points(startPoint, h) - cos(startPoint))));
//             // vectorP1.push_back(log10(abs(backwardDifference3Points(endPoint, h) - cos(endPoint))));
//         }
//         if (i == 6) {
//             oblicz_metody(startPoint, centerPoint, endPoint, h, vectorP2);
//             // vectorP2.push_back(log10(h));
//             // vectorP2.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP2.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP2.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
//             // vectorP2.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
//             // vectorP2.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
//             // vectorP2.push_back(log10(abs(forwardDifference3Points(startPoint, h) - cos(startPoint))));
//             // vectorP2.push_back(log10(abs(backwardDifference3Points(endPoint, h) - cos(endPoint))));
//         }
//         oblicz_metody(startPoint, centerPoint, endPoint, h, solutions);
//         // solutions.push_back(log10(h));
//         // solutions.push_back(log10(abs(forwardDifference(centerPoint, h) - cos(centerPoint))));
//         // solutions.push_back(log10(abs(backwardDifference(centerPoint, h) - cos(centerPoint))));
//         // solutions.push_back(log10(abs(centralDifference(centerPoint, h) - cos(centerPoint))));
//         // solutions.push_back(log10(abs(forwardDifference(startPoint, h) - cos(startPoint))));
//         // solutions.push_back(log10(abs(backwardDifference(endPoint, h) - cos(endPoint))));
//         // solutions.push_back(log10(abs(forwardDifference3Points(startPoint, h) - cos(startPoint))));
//         // solutions.push_back(log10(abs(backwardDifference3Points(endPoint, h) - cos(endPoint))));

//         h = h / static_cast<T>(1.2);
//     }

//     std::fstream plik,plik2;
//     plik.open(fileName+".txt", std::ios::out);
//     plik2.open(fileName+"_precision"+".txt", std::ios::out);
//     for (int i = 0; i < solutions.size(); i++) {
//         plik <<std::scientific<< solutions[i] << std::endl;
//     }
//     for (int i = 1; i < vectorP1.size(); i++) {
//          T a = (vectorP2[i] - vectorP1[i])/ (vectorP2[0] - vectorP1[0]);
// 		 plik2 << a << std::endl;
// 	}

//     plik.close();
//     plik2.close();
// }


// int main() {
//     calculate<float>("floatSolution", 1);
//     calculate<double>("doubleSolution", 0);

//     return 0;
// }

#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>

#define _USE_MATH_DEFINES

using namespace std;


template <typename T>
T progresywna(T x, T h) {
    return (sin(x + h) - sin(x)) / h;
}

template <typename T>
T wsteczna(T x, T h) {
    return (sin(x) - sin(x - h)) / h;
}

template <typename T>
T centralna(T x, T h) {
    return (sin(x + h) - sin(x - h)) / (static_cast<T>(2) * h);
}

template <typename T>
T progresywna3(T x, T h) {
    return (-static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x)
        + static_cast<T>(2.0) * sin(x + h)
        - static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x + h +h)) / h;
}

template <typename T>
T wsteczna3(T x, T h) {
    return ((static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x - h - h))
        - (static_cast<T>(2.0) * sin(x - h))
        + (static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x))) / h;
}
template <typename T>
void oblicz_metody(T poczatek, T srodek, T koniec, T h, vector<T>& wyniki) {
    wyniki.push_back(log10(h));

    //dwupunktowe w wezlach wewnetrznych
    wyniki.push_back(log10(abs(progresywna(srodek, h) - cos(srodek))));
    wyniki.push_back(log10(abs(wsteczna(srodek, h) - cos(srodek))));
    wyniki.push_back(log10(abs(centralna(srodek, h) - cos(srodek))));
    //dwupuntkowe w wezlach koncowych
    wyniki.push_back(log10(abs(progresywna(poczatek, h) - cos(poczatek))));
    wyniki.push_back(log10(abs(wsteczna(koniec, h) - cos(koniec))));
    //trzypunktowe w wezlach koncowych
    wyniki.push_back(log10(abs(progresywna3(poczatek, h) - cos(poczatek))));
    wyniki.push_back(log10(abs(wsteczna3(koniec, h) - cos(koniec))));
}

template <typename T>
void oblicz(string nazwaPliku,bool typ) {
    T poczatek = static_cast<T>(0.0);
    T srodek = static_cast<T>(M_PI / static_cast<T>(4.0));
    T koniec = static_cast<T>(M_PI / static_cast<T>(2.0));
    T h = static_cast<T>(0.1);
    vector<T> wyniki;

    vector<T> rzedydokladnosci1;
    vector<T> rzedydokladnosci7;

    for (int i = 0; i < 180; i++) {
        if(h<10e-15 && !typ) break;
        if(h<10e-7 && typ) break;
        if (i == 0) oblicz_metody(poczatek, srodek, koniec, h, rzedydokladnosci1);
        if (i == 6) oblicz_metody(poczatek, srodek, koniec, h, rzedydokladnosci7);
		
        oblicz_metody(poczatek, srodek, koniec, h, wyniki);

        h = h / static_cast<T>(1.2);
    }



    fstream plik,plik2;
    plik.open(nazwaPliku+".txt", ios::out);
    plik2.open(nazwaPliku+"_rzedy_dokladnosci"+".txt", ios::out);
    for (int i = 0; i < wyniki.size(); i++) {
        plik <<scientific<< wyniki[i] << endl;
    }
    for (int i = 1; i < rzedydokladnosci1.size(); i++) {
         T a = (rzedydokladnosci7[i] - rzedydokladnosci1[i])/ (rzedydokladnosci7[0] - rzedydokladnosci1[0]);
		 plik2 << a << endl;
	}

    plik.close();
    plik2.close();
}


int main() {
    oblicz<float>("floatSolution",1);
    oblicz<double>("doubleSolution",0);

    return 0;
}