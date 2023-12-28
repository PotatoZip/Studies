#include <stdio.h>

int main(){
	double a, b, n, sum = 0;
	printf("Enter start 'a' and end 'b' of your range, then enter 'n' value\n");
	scanf("%lf %lf %lf", &a, &b, &n);
	printf("Start entering 'n' values\n");
	for(int i = 0; i < n; i++){
		double x;
		scanf("%lf", &x);
		if(x >=a && x <= b)
			sum += x;
	}
	printf("%lf\n", sum);
	return 0;
}
