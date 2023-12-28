#include <iostream>
#include <stdio.h>
#include <stdlib.h>

void Inp_string(char* name, char* surname, size_t name_size, size_t surname_size);
void Print_string(char* name, char* surname);
void Proc_string(char* name, char* surname, size_t name_size, size_t surname_size);

int main() {
	char name[32], surname[64];

	Inp_string(name, surname, sizeof(name), sizeof(surname));
	Proc_string(name, surname, sizeof(name), sizeof(surname));
	Print_string(name, surname);

	system("pause");
	return 0;
}

void Inp_string(char* name, char* surname, size_t name_size, size_t surname_size) {
	printf("Enter name:\n");
	gets_s(name, name_size);
	printf("Now surname:\n");
	gets_s(surname, surname_size);
}

void Print_string(char* name, char* surname) {
	printf("%s\n%s\n", name, surname);
}

void Proc_string(char* name, char* surname, size_t name_size, size_t surname_size) {
	strcat_s(name, name_size, " ");
	strcat_s(name, name_size, surname);
	strcat_s(surname, surname_size, " ");
	strcat_s(surname, surname_size, name);
}