#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *file1, *file2;
	char ch;
	file1 = fopen("text2", "r");
	file2 = fopen("text3", "w");
	ch = fgetc(file1);
	while(ch != EOF) {
		fputc(ch, file2);
		ch = fgetc(file1);
	}
	fclose(file1);
	fclose(file2);
	return 0;
}
