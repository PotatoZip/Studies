#include <stdio.h>
#include <stdlib.h>

int main() {
	double var;
	FILE *file;
	file = fopen("text1", "w");
	printf("Enter 5 values\n");
	for(int i = 0; i < 5; i++) {
		scanf("%lf", &var);
		fprintf(file, "%lf\n", var);
	}
	fclose(file);
	file = fopen("text1", "r");
	for(int i = 0; i < 5; i++) {
		fscanf(file, "%lf", &var);
		printf("%lf\n", var);
	}

	return 0;
}
