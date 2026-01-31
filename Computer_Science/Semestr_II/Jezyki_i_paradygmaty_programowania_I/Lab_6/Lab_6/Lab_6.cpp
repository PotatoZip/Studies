#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "Structures.h"
#include "Message.h"

void function_preperation();

int main() {
	size_t items_count = 0;
	printf("Enter array size\n");
	scanf_s("%zu", &items_count);

	if (!struct_init(items_count)) {
		mess_function(MEMORY_ALLOCATION_ERROR);
	}
	//function_preperation();
	
	struct_free();
	system("pause");
	return 0;
}

void function_preperation() {

	STRUCT_STUDENT* p_struct = struct_get();
	STRUCT_STUDENT tmp;
	int no_items_filled = 0;
	char symb = 'a';

	memset((void*)&tmp, 0, sizeof(STRUCT_STUDENT));
	tmp.rok_studiow = 1;

	printf("Enter count of elements to fill\n");
	scanf_s("%d", &no_items_filled);

	for (int it = 0; it < no_items_filled; ++it) {
		for (int i = 0; i < 5; ++i) {
			tmp.surname[i] = symb;
		}
		symb++;

		struct_push(tmp);

		tmp.rok_studiow++;
	}

	struct_print();
}

