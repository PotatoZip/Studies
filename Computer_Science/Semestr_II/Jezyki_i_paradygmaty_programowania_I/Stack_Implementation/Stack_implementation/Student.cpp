#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Student.h"
#include "Messages.h"

void* StructInit(char* pName, int pYear, FIELD_OF_STUDY pCourse) {
	Student* pStudent = (Student*)malloc(sizeof(Student));
	if (!pStudent) {
		RiseErr(ALLOC_ERR);
		return NULL;
	}

	if (pStudent) {
		size_t size = strlen(pName) + 1;
		pStudent->name = (char*)malloc(size * sizeof(char));
		if (!pStudent->name) {
			RiseErr(ALLOC_ERR);
			return NULL;
		}
		strcpy_s(pStudent->name, size, pName);
		pStudent->year = pYear;
		pStudent->course = pCourse;
		pStudent->len = size - 1;
	}
	return (void*)(pStudent);
}

void* StructPush(char* name, int year, FIELD_OF_STUDY course) {
	return StructInit(name, year, course);
}

void StructFree(void* ptr) {
	Student* pStudent = (Student*)ptr;
	if (pStudent) {
		free(pStudent);
	}
}

void StructPrint(void* ptr) {
	Student* pStudent = (Student*)ptr;
	if (pStudent) {
		printf("Name: %s\nYear: %d\n", pStudent->name, pStudent->year);
		switch (pStudent->course) {
		case computer_science:
			printf("Field of study: Computer Science\n");
			break;
		case mathematics:
			printf("Field of study: Mathematics\n");
			break;
		case biology:
			printf("Field of study: Biology\n");
			break;
		case history:
			printf("Field of study: History\n");
			break;
		default:
			printf("Field of study: N/A\n");
			break;
		}
		printf("\n");
	}
}

int StructFind(void* curr, void* search) {
	Student* pCurr = (Student*)curr;
	Student* pSearch = (Student*)search;
	if (strcmp(pCurr->name, pSearch->name) == 0) {
		return 1;
	}
	return 0;
}

void StructSave(const char* filename, void* ptr) {
	Student* pStudent = (Student*)ptr;
	if (!pStudent) {
		RiseErr(ALLOC_ERR);
		return;
	}

	FILE* file = fopen(filename, "wb");
	if (file != 0) {
		RiseErr(FILE_SAVE_FAIL);
		return;
	}

	size_t size = strlen(pStudent->name) + 1;
	fwrite(&size, sizeof(size_t), 1, file);
	fwrite(pStudent->name, sizeof(char), size, file);
	fwrite(&(pStudent->year), sizeof(int), 1, file);
	fwrite(&(pStudent->course), sizeof(FIELD_OF_STUDY), 1, file);
	fwrite(&(pStudent->len), sizeof(size_t), 1, file);
	fclose(file);
}

void* StructLoad(const char* filename) {
	FILE* file = fopen(filename, "rb");
	if (file != 0) {
		RiseErr(FILE_LOAD_FAIL);
		return NULL;
	}

	Student* pStudent = (Student*)malloc(sizeof(Student));
	if (!pStudent) {
		RiseErr(ALLOC_ERR);
		fclose(file);
		return NULL;
	}

	size_t size;
	fread(&size, sizeof(size_t), 1, file);
	pStudent->name = (char*)malloc(size * sizeof(char));
	if (!pStudent->name) {
		fclose(file);
		free(pStudent);
		RiseErr(ALLOC_ERR);
		return NULL;
	}

	fread(pStudent->name, sizeof(char), size, file);
	fread(&(pStudent->year), sizeof(int), 1, file);
	fread(&(pStudent->course), sizeof(FIELD_OF_STUDY), 1, file);
	fread(&(pStudent->len), sizeof(size_t), 1, file);
	fclose(file);

	return pStudent;

}
