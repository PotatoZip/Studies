#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *file;
	char str[255];
	file = fopen("text2", "w");
	printf("Enter string line\n");
	fgets(str, sizeof(str), stdin);
	fprintf(file, "%s", str);
	fclose(file);
	return 0;
}
