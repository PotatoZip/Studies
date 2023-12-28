#include <iostream>
#include <stdlib.h>
#include <stdio.h>

int my_inp(char *p_name, char *p_surname, int *p_year, double *p_score, unsigned int sz_str);
void my_outpt(char* name, char* surname, int year, double score);
void stdin_clear();

int main(int argc, char *argv[]) {

	char name[20];
	char surname[20];
	int year;
	double score;
	my_inp(name, surname, &year, &score, sizeof(name));
	my_outpt(name, surname, year, score);

	return 0;
}

int my_inp(char *p_name, char *p_surname, int *p_year, double *p_score, unsigned int sz_str) {
	char format[64];
	printf("Enter year and score:\n");
	scanf_s("%d%lf", p_year, p_score);
	stdin_clear();

	sprintf_s(format, "%%%ds", sz_str - 1);
	printf("Enter name and surname:\n");
	scanf_s(format, p_name, sz_str);
	scanf_s(format, p_surname, sz_str);
	stdin_clear();

	return 0;
}

void my_outpt(char* name, char* surname, int year, double score) {
	printf("\n\nName: %s\nSurname: %s\nYear: %d\nScore: %lf\n", name, surname, year, score);
}

void stdin_clear() {
	int ch;
	printf("wyczyszczamy stdin:   ");
	while ((ch = getchar()) != '\n')
	{
		printf("%c", ch);
	}
	printf(" ; \n");
}