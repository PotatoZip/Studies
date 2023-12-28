#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define li 10

double series(double x){
	double series1 = 1, series2 = 1;
	for(int i = 1; i <= li; i++){
		series1 *= -((double)(2*i+1)/(double)(2*i))*x;
		series2 += series1;
	}
	return series2;
}
int main(){
	double a, b, sub_range, step, x;
	printf("Enter start 'a' and end 'b' of your range, then enter subrange count\n");
	scanf("%lf %lf %lf", &a, &b, &sub_range);
	step = (b-a)/sub_range;
	printf("step = %6.2lf\n\n\n", step);
	printf("    ---------------------------------------------------\n");
	printf("	x   	     series(x)	        (1+x)^(-3/2)(x)\n    ---------------------------------------------------\n");
	for(x = a; x <= b; x += step){
		printf("    %10.2lf         %7.4lf               %7.4lf\n", x, series(x), pow(1/(1+x), 3./2));
	}
	printf("    ---------------------------------------------------\n");

	return 0;
}
