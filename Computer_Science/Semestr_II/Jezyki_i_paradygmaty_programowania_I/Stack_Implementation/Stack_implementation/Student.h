#pragma once
#pragma warning (disable : 4996)

enum FIELD_OF_STUDY {
	computer_science,
	mathematics,
	biology,
	history
};

struct Student {
	char* name;
	int year;
	FIELD_OF_STUDY course;
	size_t len;
};

void* StructInit(char* pName, int pYear, FIELD_OF_STUDY pCourse);
void* StructPush(char* pName, int pYear, FIELD_OF_STUDY pCourse);
void StructFree(void* ptr);
void StructPrint(void* ptr);
int StructFind(void* curr, void* search);
void StructSave(const char *filename, void* ptr);
void* StructLoad(const char* filename);