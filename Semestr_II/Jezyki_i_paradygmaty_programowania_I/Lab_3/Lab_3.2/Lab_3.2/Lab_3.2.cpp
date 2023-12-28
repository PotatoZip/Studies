#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int my_inpt(double* p_a, double* p_b, double* p_c, double* p_d);
double my_calc(double a, double b, double c, double d, int num);
void my_outpt(double f1, double f2, double f3);

int main() {
	double a, b, c, d;
	my_inpt(&a, &b, &c, &d);
	double f1 = my_calc(a, b, c, d, 1);
	double f2 = my_calc(a, b, c, d, 2);
	double f3 = my_calc(a, b, c, d, 3);
	my_outpt(f1, f2, f3);

	system("pause");
	return 0;
}

int my_inpt(double* p_a, double* p_b, double* p_c, double* p_d) {

	printf("Enter four double values:\n");
	scanf_s("%lf%lf%lf%lf", p_a, p_b, p_c, p_d);

	return 0;
}

double my_calc(double a, double b, double c, double d, int num) {
	if (num == 1) {
		return (a + b) / (c - d) - (c + d) / a + b;
	}
	else if (num == 2) {
		return a - sin(b / c + d);
	}
	else if (num == 3) {
		return log(a / (b - c)) + d;
	}
}

void my_outpt(double f1, double f2, double f3) {
	printf("Function_1: %lf\nFunction_2: %lf\nFunction_3: %lf\n", f1, f2, f3);
}