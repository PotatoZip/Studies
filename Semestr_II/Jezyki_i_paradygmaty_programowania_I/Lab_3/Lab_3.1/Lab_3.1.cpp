#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void inputs(double * p_x, double * p_eps);
double get_sum(double x, double j);
void print_inputs(double x, double eps);
double factorial(double n);

int main() {
	double sum = 0, x, err, eps;
	int n = 0;
	inputs(&x, &eps);
	double sum_exact = exp(x);
	printf("\n\nWIiT\nWiktor Zmiendak\n");
	print_inputs(x, eps);
	printf("\tn\t|\tSn\t\t|\terr\n");
	do {
		sum += get_sum(x, n);
		err = abs(sum - sum_exact) / abs(sum_exact);
		printf("\t%d\t|\t%lf\t|\t%lf\n", n, sum, err);
		n++;
	} while (eps < err);
	
	system("pause");
	return 0;
}

void inputs(double* p_x, double* p_eps) {
	printf("Enter x - value, eps - max approximation error\n");
	scanf_s("%lf%lf", p_x, p_eps);
}

double get_sum(double x, double j) {
	return pow(x,j)/factorial(j);
}

void print_inputs(double x, double eps) {
	printf("x: %lf, n: %lf\n", x, eps);
}

double factorial(double n) {
	double retval = 1;
	for (int i = 1; i < n + 1; i++) {
		retval *= i;
	}
	return retval;
}


