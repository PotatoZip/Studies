#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#define lp 100000

double c_od,c_do;

double f3(double x) {
        return x/(x*x*x*x + 1);     
}

double f4(double x) {

        return x*x*x*x*x*log(x);
}


double prostokaty(double( *f)(double)) {
        double krok, p, suma=0;
        krok=(c_do-c_od)/lp;
        for(p=c_od; p<c_do; p+=krok)
                suma+=(*f)(p);
        suma *= krok;
        return suma;      
}

double trapezy(double (*f)(double)) {
        double krok, p, suma = 0;
        krok = (c_do - c_od)/lp;
        for(p = c_od + krok; p < c_do; p += krok) {
                suma += (*f)(p) + (*f)(p + krok);
        }
        suma *= (1./2)*krok;
        return suma;
}
       
double mc(double(*f)(double)) {
        double p, ymin = 0, ymax = 0, Nl = 0, krok, ff, range, area, suma = 0;
        krok = (c_do - c_od)/lp;
        range = c_do - c_od;
        for(p = c_od; p <= c_do; p +=krok) {
                ff = (*f)(p);
                if(ff > ymax) {
                        ymax = ff;
                } 
                else if(ff < ymin) {
                        ymin = ff;
                }
        }
        if(ymax > 0 && ymin > 0) {
                ymin = 0;
        }
        else if(ymax < 0 && ymin < 0) {
                ymax = 0;
        }
        area = (ymax - ymin)*range;
        for(int i = 1; i <= lp; i++) {
                double x = rand();
                x = x/RAND_MAX*range + c_od;
                double y = rand();
                y = y/RAND_MAX*(ymax - ymin) + ymin;
                ff = (*f)(x);
                if(y > 0 && ff > y) {
                        Nl++;
                }
                else if(y < 0 && ff < y) {
                        Nl--;
                }
        }
        suma = (Nl/lp)*area;

        return suma;
}

