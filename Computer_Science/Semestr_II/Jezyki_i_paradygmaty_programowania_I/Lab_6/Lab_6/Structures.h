#pragma once

struct STRUCT_STUDENT {
	char surname[256];
	enum KIERUNEK_STUD kierunek;
	int rok_studiow;
};

enum KIERUNEK_STUD {
	KIERUNEK_MATEMATYKA,
	KIERUNEK_INFORMATYKA,
	KIERUNEK_FIZYKA_TECHNICZNA
};

int struct_init(size_t len_str);
void struct_free();
STRUCT_STUDENT* struct_get();
int struct_push(STRUCT_STUDENT ob);
void struct_print();
size_t struct_size();