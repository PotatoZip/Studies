#include <iostream>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
	int var_int;
	long var_long;
	unsigned long var_unsigned_long;
	float var_float;
	double var_double1, var_double2;
	printf("Wprowadz 3 wartosci calkowite:\n");
	scanf_s("%d%ld%u", &var_int, &var_long, &var_unsigned_long);
	printf("Wprowadz 3 wartosci rzeczywiste:\n");
	scanf_s("%f%lf%lf", &var_float, &var_double1, &var_double2);
	printf("\n|Typ\t\t|\t\tLiczby calkowite\n-----------------------------------------------------------\n");
	printf("|int\t\t|%d|%-12d|%12d|\n", var_int, var_int, var_int);
	printf("|long\t\t|%ld|%-14ld|%+14ld|\n", var_long, var_long, var_long);
	printf("|unsigned long\t|%u|%-14u|%14u|\n", var_unsigned_long, var_unsigned_long, var_unsigned_long);
	printf("\n|Typ\t\t|\t\tLiczby rzeczywiste\n-----------------------------------------------------------\n");
	printf("|float\t|%f|%-14.3f|%e|%+14.4e|\n", var_float, var_float, var_float, var_float);
	printf("|double\t|%lf|%-14.3lf|%le|%+14.4le|\n", var_double1, var_double1, var_double1, var_double1);
	printf("|double\t|%lf|%-14.3lf|%le|%+14.4le|\n", var_double2, var_double2, var_double2, var_double2);

	int ch;
	while ((ch = getchar()) != EOF)
		;
	return 0;
}