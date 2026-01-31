#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	char str[100];
	printf("Enter text\n");
	scanf("%s", str);
	for(int i = strlen(str); i >= 0; i--) {
		printf("%c", str[i]);
	}
	printf("\n");

	return 0;
}
