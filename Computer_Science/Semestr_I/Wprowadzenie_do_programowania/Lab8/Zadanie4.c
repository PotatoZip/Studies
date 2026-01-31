#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
	while(1) {
		char ans, d_code[100], e_code[100];
		printf("Do you want to encript [e] or decript [d] your code?\n");
		scanf(" %c", &ans);
		if(ans == 'e') {
			printf("Enter your code\n");
			scanf(" %[^\n]", d_code);
			int d_len = strlen(d_code);
			for(int i = 0; i < d_len; i++) {
				if(d_code[i] == 'a')
					d_code[i] = 'x';
				else if(d_code[i] == 'b')
					d_code[i] = 'y';
				else if(d_code[i] == 'c')
					d_code[i] = 'z';
				else if(d_code[i] == 'A')
					d_code[i] = 'X';
				else if(d_code[i] == 'B')
					d_code[i] = 'Y';
				else if(d_code[i] == 'C')
					d_code[i] = 'Z';
				else if(d_code[i] == ' ')
					continue;
				else
					d_code[i] -= 3;
			}
			printf("Encripted text:\n%s\n", d_code);
		}
		else if(ans == 'd') {
			printf("Enter your code\n");
			scanf(" %[^\n]", e_code);
			int e_len = strlen(e_code);
			for(int i = 0; i < e_len; i++) {
				if(e_code[i] == 'x')
					e_code[i] = 'a';
				else if(e_code[i] == 'y')
					e_code[i] = 'b';
				else if(e_code[i] == 'z')
					e_code[i] = 'c';
				else if(e_code[i] == 'X')
					e_code[i] = 'a';
				else if(e_code[i] == 'Y')
					e_code[i] = 'B';
				else if(e_code[i] == 'Z')
					e_code[i] = 'C';
				else if(e_code[i] == ' ')
					continue;
				else
					e_code[i] += 3;
			}
			printf("Cripted text:\n%s\n", e_code);
		}
		else {
			printf("Wrong input\n");
			continue;
		}
		char ans_c;
		printf("Do you want to encript/cript another text? [y]\n");
		scanf(" %c", &ans_c);
		if(ans_c == 'y') {
			continue;
		}

		break;
	}

	return 0;
}
