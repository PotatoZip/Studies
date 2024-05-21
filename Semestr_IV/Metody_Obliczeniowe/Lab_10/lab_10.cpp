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

//Second Part
using namespace std;
double BME(double, double, double, double);
double PME(double, double, double, double);
double PMT(double, double, double, double);
void get_actual(double, double, double);
void errors(double, double, double, double, double);
double actual(double t) {
    return 1.0 - exp(-10.0 * (t + atan(t)));
}
double f_pom(double t) {
    return (10.0 * t * t + 20.0) / (t * t + 1.0);
}
double f(double t, double yt) {
    return (1.0 - yt) * f_pom(t);
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
    for (double t = 0; t < 10; t += 0.01) {
        rozwAnalityczne = analiticSolution(t);
        euler_b = bme(0.2, t);
        out_ns << std::setw(dl_) << t << std::setw(dl_) << rozwAnalityczne << std::setw(dl_) << euler_b << std::endl;
    }
    out_ns.close();

    //Second Part
    double delta_t = 0.001;
    double start = 0.0, finish = 1.0;
    double cond = 0.0;
    get_actual(delta_t, start, finish);
    BME(delta_t, start, finish, cond);
    PME(delta_t, start, finish, cond);
    PMT(delta_t, start, finish, cond);
    double lim = 1e-10;
    errors(delta_t, start, finish, cond, lim);


    return 0;
}

//Second Part

void get_actual(double delta_t, double start, double finish) {
    ofstream actual_values;
    actual_values.open("wartosci_dokladne.txt");
    while (start < finish) {
        actual_values << start << " " << actual(start) << endl;
        start += delta_t;
    }
}

double BME(double delta_t, double start, double finish, double yk) {
    ofstream BME_val;
    BME_val.open("BME.txt");
    double yk1;
    double maks_err = 0.0, local_err;
    while (start <= finish) {
        BME_val << start << " " << yk << endl;
        yk1 = yk + f(start, yk) * delta_t;
        start += delta_t;
        yk = yk1;
        local_err = abs(yk - actual(start));
        if (maks_err < local_err) {
            maks_err = local_err;
        }
    }
    return maks_err;
}
double PME(double delta_t, double start, double finish, double yk) {
    ofstream PME_val;
    PME_val.open("PME.txt");
    double yk1;
    double maks_err = 0.0, local_err;
    while (start <= finish) {
        PME_val << start << " " << yk << endl;
        yk1 = (yk + f_pom(start + delta_t) * delta_t) / (1.0 + f_pom(start +
            delta_t) * delta_t);
        start += delta_t;
        yk = yk1;
        local_err = abs(yk - actual(start));
        if (maks_err < local_err) {
            maks_err = local_err;
        }
    }
    return maks_err;
}
double PMT(double delta_t, double start, double finish, double yk) {
    ofstream PMT_val;
    PMT_val.open("PMT.txt");
    double yk1;
    double maks_err = 0.0, local_err;
    while (start <= finish) {
        PMT_val << start << " " << yk << endl;
        yk1 = (yk + (delta_t / 2.0 * f_pom(start)) + (delta_t / 2.0 *
            f_pom(start + delta_t)) - yk * delta_t / 2.0 * f_pom(start)) / ((delta_t /
            2.0) * f_pom(start + delta_t) + 1.0);
        start += delta_t;
        yk = yk1;
        local_err = abs(yk - actual(start));
        if (maks_err < local_err) {
            maks_err = local_err;
        }
    }
    return maks_err;
}
void errors(double delta_t, double start, double finish, double cond, double lim) {
    ofstream BME_err, PME_err, PMT_err;
    BME_err.open("BME_err.txt");
    PME_err.open("PME_err.txt");
    PMT_err.open("PMT_err.txt");
    double BME_err_val, PME_err_val, PMT_err_val;
    while (delta_t >= lim) {
        BME_err_val = BME(delta_t, start, finish, cond);
        PME_err_val = PME(delta_t, start, finish, cond);
        PMT_err_val = PMT(delta_t, start, finish, cond);
        BME_err << log10(delta_t) << " " << log10(BME_err_val) << endl;
        PME_err << log10(delta_t) << " " << log10(PME_err_val) << endl;
        PMT_err << log10(delta_t) << " " << log10(PMT_err_val) << endl;
        delta_t /= 2.0;
    }
}