#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *file;
	char str[255];
	file = fopen("text5", "w");
	printf("Enter your text\n");
	fgets(str, sizeof(str), stdin);
	fprintf(file, "%s", str);
	fclose(file);

	int freq[37];
	file = fopen("text5", "r");
	char ch;
	while(!feof(file)) {
		ch = fgetc(file);
		if(ch == ' ')
			continue;
		if(ch > 47 && ch < 58) {
			freq[ch - 22]++;
		}
		freq[ch - 'a']++;
	}
	for(int i = 0; i < 26; i++) {
		printf("Character %c appears %d times\n", i+65, freq[i]);
	}
	for(int i = 0; i < 10; i++) {
		printf("Character %d appears %d times\n", i, freq[i+26]);
	}
	fclose(file);

	return 0;
}
