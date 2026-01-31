#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *file;
	char str[255];
	file = fopen("text4", "w");
	printf("Enter text to file\n");
	fgets(str, sizeof(str),stdin);
	fprintf(file, "%s", str);
	fclose(file);

	file = fopen("text4", "r");
	int count = -1;
	char ch = fgetc(file);
	while( ch != EOF) {
		if(ch == ' ') {
			ch = fgetc(file);
			continue;
		}
		ch = fgetc(file);
		count++;
	}
	fclose(file);
	printf("This file contain %d characters\n", count);
	return 0;
}
