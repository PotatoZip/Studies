#include <stdio.h>
#include <math.h>

int main(){
	int n,x;
	double art = 0,geo = 1;
	printf("Enter n value then n values\n");
	scanf("%d", &n);
	for(int i = 0; i < n; i++){
		scanf("%d", &x);
		art += x;
		geo *= x;
	}
	art /= n;
	geo = pow(geo,1./n);
	printf("Arythmetic mean is: %lf\nGeometric mean is: %lf\n", art, geo);
	return 0;
}
