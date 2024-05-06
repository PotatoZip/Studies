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
T forwardDifference3Point(T x, T h) {
    return ((static_cast<T>(1.0) / static_cast<T>(2.0) * sin(x - h - h))
        - (static_cast<T>(2.0) * sin(x - h))
        + (static_cast<T>(3.0) / static_cast<T>(2.0) * sin(x))) / h;
}
template <typename T>
void calculate2(T poczatek, T srodek, T koniec, T h, vector<T>& wyniki) {
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
    wyniki.push_back(log10(abs(forwardDifference3Point(koniec, h) - cos(koniec))));
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
        if (i == 0) calculate2(poczatek, srodek, koniec, h, rzedydokladnosci1);
        if (i == 6) calculate2(poczatek, srodek, koniec, h, rzedydokladnosci7);
		
        calculate2(poczatek, srodek, koniec, h, wyniki);

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
    oblicz<float>("wynikfloat",1);
    oblicz<double>("wynikdouble",0);

    return 0;
}