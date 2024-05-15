#include <iostream>
#include <cmath>
#include <iomanip>
#include <fstream>

int dl_ = 15;

double analiticSolution(double t) { return 1 - exp(-10.0 * (t + atan(t))); }

double bme(double step, double tmax) {
    double y = 0.0;
    for (double t = 0.0; t < tmax; t += step) { y = y - step * (y - 1.0) * (10.0 * t * t + 20.0) / (t * t + 1.0); }
    return y;
}

double pme(double step, double tmax) {
    double y = 0.0;
    double fraction;
    for (double t = 0.0; t < tmax; t += step) {
        fraction = (10.0 * (t + step) * (t + step) + 20.0) / ((t + step) * (t + step) + 1.0);
        y = (y + step * fraction) / (1 + step * fraction);
    }
    return y;
}

double mt(double step, double tmax) {
    double y = 0.0, u1, u2;
    for (double t = 0.0; t < tmax; t += step) {
        u1 = ((10.0 * t * t + 20.0) / (t * t + 1.0));
        u2 = (10.0 * (t + step) * (t + step) + 20.0) / ((t + step) * (t + step) + 1.0);
        y = ((-step / 2.0) * (u1 * (y - 1.0) - u2) + y) / (1.0 + (step / 2.0) * u2);
    }
    return y;
}

double mtError(double step, int N) {
    double maxBlad = 0.0, t = 0, y = 0.0;
    double exactValue, u1, u2;
    for (int i = 0; i < N; i++) {
        u1 = ((10.0 * t * t + 20.0) / (t * t + 1.0));
        u2 = (10.0 * (t + step) * (t + step) + 20.0) / ((t + step) * (t + step) + 1.0);
        y = ((-step / 2.0) * (u1 * (y - 1.0) - u2) + y) / (1.0 + (step / 2.0) * u1);
        exactValue = analiticSolution(t);
        if (fabs(exactValue - y) > maxBlad)
            maxBlad = fabs(exactValue);
        t += step;
    }
    return maxBlad;
}

double bmeError(double step, int n) {
    double maxBlad = 0.0, t = 0, y = 0.0, exactValue;
    for (int i = 0; i < n; i++) {
        y = y - step * (y - 1.0) * ((10.0 * t * t + 20.0) / (t * t + 1.0));
        exactValue = analiticSolution(t);
        if (fabs(exactValue - y) > maxBlad)
            maxBlad = fabs(exactValue - y);
        t += step;
    }
    return maxBlad;
}


double pmeError(double step, int n) {
    double maxBlad = 0.0, y = 0.0, t = 0, exactValue, fraction;
    for (int i = 0; i < n; i++) {
        fraction = (10.0 * (t + step) * (t + step) + 20.0) / ((t + step) * (t + step) + 1.0);
        y = (y + step * fraction) / (1 + step * fraction);
        exactValue = analiticSolution(t);
        if (fabs(exactValue - y) > maxBlad)
            maxBlad = fabs(exactValue - y);
        t += step;
    }
    return maxBlad;
}

int main() {
    double step = 0.1, euler_b, euler_p, trapezow, rozwAnalityczne;
    int tmax = 100;
    std::fstream out_b, out_s, out_ns;
    out_b.open("errors.txt", std::fstream::out);
    for (step; step > 1e-18; step *= .9) {
        euler_b = log10(bmeError(step, tmax));
        euler_p = log10(pmeError(step, tmax));
        trapezow = log10(mtError(step, tmax));
        out_b << std::setw(dl_) << log10(step) << std::setw(dl_) << euler_b << std::setw(dl_) << euler_p << std::setw(dl_) << trapezow << std::endl;
    }
    out_b.close();
    step = 0.01;
    out_s.open("stable.txt", std::fstream::out);
    for (double t = 0; t < 1; t += 0.01) {
        rozwAnalityczne = analiticSolution(t);
        euler_b = bme(step, t);
        euler_p = pme(step, t);
        trapezow = mt(step, t);
        out_s << std::setw(dl_) << t << std::setw(dl_) << rozwAnalityczne << std::setw(dl_) << euler_b << std::setw(dl_) << euler_p << std::setw(dl_) << trapezow << std::endl;
    }
    out_s.close();
    out_ns.open("unstable.txt", std::fstream::out);
    for (double t = 0; t < 1; t += 0.01) {
        rozwAnalityczne = analiticSolution(t);
        euler_b = bme(0.2, t);
        out_ns << std::setw(dl_) << t << std::setw(dl_) << rozwAnalityczne << std::setw(dl_) << euler_b << std::endl;
    }
    out_ns.close();
}