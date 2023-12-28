#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "Structures.h"
#include "Message.h"

static STRUCT_STUDENT* p_struct = NULL;
static size_t last_pos = 0;

int struct_init(size_t elements) {
	if (!p_struct) {
		p_struct = (STRUCT_STUDENT*)malloc(elements * sizeof(STRUCT_STUDENT));
		if (!p_struct) {
			return 0;
		}
		memset((void*)p_struct, 0, elements * sizeof(STRUCT_STUDENT));
		last_pos = 0;
		return 1;
	}
	return 0;
}

void struct_free() {
	if (p_struct) {
		free(p_struct);
	}
	p_struct = NULL;
}

STRUCT_STUDENT* struct_get() {
	return p_struct;
}

int struct_push(STRUCT_STUDENT ob) {
	size_t max_pos = _msize(p_struct) / sizeof(STRUCT_STUDENT);
	if (last_pos >= max_pos) {
		max_pos += max_pos;
		p_struct = (STRUCT_STUDENT*)realloc(p_struct, max_pos * sizeof(STRUCT_STUDENT));
		if (!p_struct) {
			return 0;
		}
	}
	p_struct[last_pos].rok_studiow = ob.rok_studiow;
	strcpy_s(p_struct[last_pos].surname, sizeof(p_struct[last_pos].surname), ob.surname);
	return 1;
}

STRUCT_STUDENT* struct_pop() {
	if (last_pos > 0) {
		return &p_struct[--last_pos];
	}
	return NULL;
}

void struct_print() {
	for (int i = 0; i < last_pos; ++i) {
		printf("%s\n", p_struct[i].surname);
		printf("%d\n", p_struct[i].rok_studiow);
		//printf("%s\n", p_struct[i].kierunek);
	}
}

size_t struct_size() {
	return last_pos;
}