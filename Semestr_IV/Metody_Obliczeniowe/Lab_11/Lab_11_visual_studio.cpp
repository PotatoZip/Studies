#include <iostream>
#include <fstream>
#include "calerf.h"
#include "cmath"
using namespace std;
double D = 1.0;
double T_MAX = 2.0;
double T_MIN = 0.0;
double LAMBDA_LAASONEN = 1.0;
double LAMBDA_KMB = 0.4;
double H = 0.1;
double A = 6.0 * sqrt(D * T_MAX);
double X_MIN = -A;
double X_MAX = A;
double** inicjalizacjaMacierzy(int n, int m) {
auto** macierz = new double*[n];
for (int i = 0; i < n; i++) {
macierz[i] = new double[m];
}
return macierz;
}
void zapisWektoraDoPliku(double* wektor, int n, const string& nazwaPliku)
{
fstream plik(nazwaPliku.c_str(), ios::out);
if (plik.is_open()) {
for (int i = 0; i < n; i++) {
plik << wektor[i] << endl;
}
}
}
void macierzDoPliku(double** macierz, int n, int m, const string&
nazwaPliku) {
fstream plik(nazwaPliku.c_str(), ios::out);
if (plik.is_open()) {
for (int i = 0; i < n; ++i) {
for (int j = 0; j < m; ++j) {
plik << macierz[i][j] << ";";
}
plik << endl;
}
}
plik.close();
}
double wartoscDokladna(double x, double t) {
return calerf::ERFCL((x) / (2.0*sqrt(D*t)))/2.0;
}
void warunekPoczatkowy(double** macierz, int m) {
double x = X_MIN;
for (int i = 0; i < m; i++) {
if (x < 0) {
macierz[0][i] = 1.0;
}
else {
macierz[0][i] = 0.0;
}
x += H;
}
}
void warunekBrzegowy(double** macierz, int n, int m) {
for (int i = 0; i < n; i++) {
macierz[i][0] = 1.0;
macierz[i][m - 1] = 0.0;
}
}
double obliczDT(double lambda, double h, double d) {
return (lambda*h*h) / d;
}
double** rozwiazanieAnalityczne(int n, int m, double dt) {
double** analityczne = inicjalizacjaMacierzy(n, m);
double x = X_MIN;
double t = T_MIN;
for (int i = 0; i < n; i++) {
for (int j = 0; j < m; j++) {
analityczne[i][j] = wartoscDokladna(x, t);
x += H;
}
x = X_MIN;
t += dt;
}
return analityczne;
}
double** rozwiazanieKMB(int n, int m) {
double** wynik = inicjalizacjaMacierzy(n, m);
warunekPoczatkowy(wynik, m);
warunekBrzegowy(wynik, n, m);
for (int i = 1; i < n; i++) {
for (int j = 1; j < m - 1; j++) {
wynik[i][j] = LAMBDA_KMB * (wynik[i-1][j-1] -
2.0*wynik[i-1][j] + wynik[i-1][j+1]) + wynik[i-1][j];
}
}
return wynik;
}
void pierwszyKrokThomasa(double* u, double* l, double* d, double* b, int
n){
for (int i = 1; i < n; i++){
d[i] = d[i] - ((l[i - 1] / d[i - 1]) * u[i - 1]);
b[i] = b[i] - ((l[i - 1] / d[i - 1]) * b[i - 1]);
}
}
void drugiKrokThomasa(double* u, double* d, double* b, double* x, int n){
x[n - 1] = b[n - 1] / d[n - 1];
for (int i = n - 2; i >= 0; i--) {
x[i] = (b[i] - u[i] * x[i + 1]) / d[i];
}
}
void algorytmThomasa(double** a,double *b, double *x,int m){
auto l = new double[m];
auto d = new double[m];
auto u = new double[m];
d[0] = a[0][0];
for (int i = 1; i < m - 1; i++) {
u[i]=a[i][i + 1];
d[i] = a[i][i];
l[i-1] = a[i][i - 1];
}
d[m - 1] = a[m-1][m-1];
pierwszyKrokThomasa(u,l,d,b,m);
drugiKrokThomasa(u,d,b,x,m);
}
double* residuum(double** a, double* b, double* x, int m){
double sum = 0.0;
auto tmp = new double[m];
for (int i = 0; i < m; i++) {
for (int j = 0; j < m; j++) {
sum += a[i][j] * x[j];
}
tmp[i] = sum - b[i];
sum = 0.0;
}
return tmp;
}
double est(double* wektor1, double* wektor2, int n){
double max = abs(wektor1[0] - wektor2[0]);
for (int i = 1; i < n; i++){
if (abs(wektor1[i] - wektor2[i]) > max)
max = abs(wektor1[i] - wektor2[i]);
}
return max;
}
double maksymalnaWartoscWektora(double* wektor, int n) {
double max = fabs(wektor[0]);
for (int i = 1; i < n; i++) {
if (max < fabs(wektor[i])) {
max = fabs(wektor[i]);
}
}
return max;
}
void jacobi(double** B, double* b, double* x, int m) {
double tol = 1e-8;
auto xTmp = new double[m];
double sum;
for (int iteracja = 0; iteracja < 100; iteracja++) {
for (int i = 0; i < m; i++) {
sum = 0.0;
for (int j = 0; j < m; j++) {
if (j != i) {
sum += (B[i][j] * x[j]);
}
}
xTmp[i] = (-sum + b[i]) / B[i][i];
}
for (int i = 0; i < m; i++) {
x[i] = xTmp[i];
}
if ((fabs((maksymalnaWartoscWektora(residuum(B, b, x, m), m))) <
tol) && (fabs((est(xTmp, x, m))) < tol)) break;
}
}
double** rozwiazanieLaasonen(int n, int m,string funkcja) {
auto rozwiazanie = inicjalizacjaMacierzy(n, m);
warunekPoczatkowy(rozwiazanie, m);
warunekBrzegowy(rozwiazanie, n, m);
auto b = new double[m];
auto wynik = new double[m];
for (int i = 0; i < m; i++) {
b[i] = 0.0;
wynik[i] = 0.0;
}
auto a = inicjalizacjaMacierzy(m, m);
for (int i = 0; i < m; i++) {
for (int j = 0; j < m; j++) {
a[i][j] = 0.0;
}
}
for (int k = 1; k < n; k++) {
a[0][0] = 1.0;
b[0] = rozwiazanie[k - 1][0];
for (int i = 1; i < m - 1; i++) {
a[i][i + 1] = LAMBDA_LAASONEN;
a[i][i] = -(1.0 + 2.0 * LAMBDA_LAASONEN);
a[i][i - 1] = LAMBDA_LAASONEN;
b[i] = -rozwiazanie[k - 1][i];
}
b[m - 1] = 0.0;
a[m - 1][m - 1] = 1.0;
if(funkcja == "j"){
jacobi(a, b, wynik, m);
}else{
algorytmThomasa(a,b,wynik,m);
}
for (int i = 1; i < m - 1; i++) {
rozwiazanie[k][i] = wynik[i];
}
}
return rozwiazanie;
}
double* bledy(double** rozwiazanieAnalityczne, double**
rozwiazanieNumeryczne, int n, int m) {
double** bledy = inicjalizacjaMacierzy(n, m);
for (int i = 0; i < n; i++) {
for (int j = 0; j < m; j++) {
bledy[i][j] = fabs(rozwiazanieNumeryczne[i][j] -
rozwiazanieAnalityczne[i][j]);
}
}
auto maxBlad = new double[n];
for (int i = 0; i < n; i++) {
maxBlad[i] = maksymalnaWartoscWektora(bledy[i], m);
}
return maxBlad;
}
double* osX(int m) {
auto x = new double[m];
x[0] = X_MIN;
for (int i = 1; i < m; i++) {
x[i] = x[i - 1] + H;
}
return x;
}
double* osT(double dt, int n) {
auto t = new double[n];
t[0] = T_MIN;
for (int i = 1; i < n; i++) {
t[i] = t[i - 1] + dt;
}
return t;
}
void kmb(){
double dt = obliczDT(LAMBDA_KMB, H, D);
int n = ((T_MAX - T_MIN) / dt);
int m = ((X_MAX - X_MIN) / H);
double** analityczne = rozwiazanieAnalityczne(n, m, dt);
double** numeryczne = rozwiazanieKMB(n, m);
macierzDoPliku(numeryczne, n, m, "kmb.txt");
zapisWektoraDoPliku(bledy(analityczne, numeryczne, n, m), n,
"blady_kmb.txt");
zapisWektoraDoPliku(osT(dt, n), n, "os_t_kmb.txt");
zapisWektoraDoPliku(osX(m), m, "os_x_kmb.txt");
}
void laasonen(){
double dt = obliczDT(LAMBDA_LAASONEN, H, D);
int n = ((T_MAX - T_MIN) / dt);
int m = ((X_MAX - X_MIN) / H);
double** analityczne = rozwiazanieAnalityczne(n, m, dt);
double** numeryczneThomas = rozwiazanieLaasonen(n, m,"t");
double** numeryczneJacobi = rozwiazanieLaasonen(n, m,"j");
macierzDoPliku(analityczne, n, m, "analityczne.txt");
macierzDoPliku(numeryczneJacobi, n, m, "laasonen_jacobi.txt");
macierzDoPliku(numeryczneThomas, n, m, "laasonen_thomas.txt");
zapisWektoraDoPliku(bledy(analityczne, numeryczneJacobi, n, m), n,
"bledy_laasonen_jacobi.txt");
zapisWektoraDoPliku(bledy(analityczne, numeryczneThomas, n, m), n,
"bledy_laasonen_thomas.txt");
zapisWektoraDoPliku(osX(m), m, "os_x_laasonen.txt");
zapisWektoraDoPliku(osT(dt, n), n, "os_t_laasonen.txt");
}
int main() {
kmb();
laasonen();
return 0;
}