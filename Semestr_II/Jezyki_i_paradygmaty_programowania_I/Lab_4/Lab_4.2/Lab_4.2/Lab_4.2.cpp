#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "math.h"

void menu_option(char* str);
void input_value(int* arr, int digits);
void find_integer(int* arr_to_write, int* arr_to_find, int write_digits, int find_digits);
int value_digits(int value);

int main() {
	int arr_to_write[256];
	int arr_to_find[64];
	char ch_tmp = ' ';
	while (ch_tmp != 'e') {
		menu_option(&ch_tmp);
		int write_digits = 0;
		int find_digits = 0;
		switch (ch_tmp) {
		case 'w':
			input_value(arr_to_write, write_digits);
			break;
		case 'c':
			input_value(arr_to_find, find_digits);
			break;
		case 'f':
			find_integer(arr_to_write, arr_to_find, write_digits, find_digits);
			break;
		case 'e':
			break;
		default:
			printf("Wrong input\n");
		};
	}

	system("pause");
	return 0;
}

void menu_option(char* str) {
	const char* menu_lines[] = {
		"Enter main integer value - w",
		"Enter integer to find    - c",
		"Find integer             - f",
		"Exit                     - e"
	};

	for (int i = 0; i < 4; i++) {
		printf("%s\n", menu_lines[i]);
	}
	scanf_s(" %c", str);
}

void input_value(int* arr, int digits) {
	int value;
	scanf_s("%d", &value);
	digits = value_digits(value);
	int i = (value == 0) ? 1 : log10(value) + 1;
	while (value != 0) {
		arr[i] = value % 10;
		value /= 10;
		i--;
	}
}

void find_integer(int* arr_to_write, int* arr_to_find, int write_digits,int find_digits) {
	if (write_digits < find_digits) {
		printf("Can't find reps in main integer\n");
	}
	printf("ok\n");
}

int value_digits(int value) {
	int digits = 0;
	while (value != 0) {
		value /= 10;
		digits++;
	}
	return digits;
}