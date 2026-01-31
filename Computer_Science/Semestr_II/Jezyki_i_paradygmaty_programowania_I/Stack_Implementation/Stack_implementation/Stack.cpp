#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Stack.h"
#include "Student.h"
#include "Messages.h"

Stack* top = NULL;
freeData pFree;

void StackInit(freeData ptrFree) {
	top = NULL;
	pFree = ptrFree;
}

Stack* StackPush(void* ptr) {
	Stack* curr = (Stack*)malloc(sizeof(Stack));
	if (!curr) {
		RiseErr(ALLOC_ERR);
		return NULL;
	}
	curr->pData = ptr;
	curr->next = top;
	top = curr;
	return curr;
}

void StackFree() {
	Stack* curr = top;
	Stack* next = NULL;
	while (curr) {
		(*pFree)(curr->pData);
		next = curr;
		curr = curr->next;
		free(next);
	}
	top = NULL;
}

void *StackPop() {
	Stack pop;
	if (!top) {
		RiseErr(STACK_UNDERFLOW);
		return NULL;
	}
	else {
		Stack* next = top->next;
		pop.pData = top->pData;
		free(top);
		top = next;
		return pop.pData;
	}
}

Stack* StackTop() {
	return top;
}

void* StackFind(void* search, compData pComp, int first) {
	static Stack* ptr;
	Stack* pTmp = NULL;
	if (first) {
		ptr = top;
	}
	if (ptr == NULL) {
		RiseErr(STACK_UNDERFLOW);
		return NULL;
	}
	while (ptr) {
		if (!(*pComp)(ptr->pData, search)) {
			ptr = ptr->next;
		}
		else {
			pTmp = ptr;
			ptr = ptr->next;
			return pTmp->pData;
		}
	}
	return NULL;
}

void StackSave(const char* filename) {
	FILE* file = fopen(filename, "wb");
	if (file == NULL) {
		RiseErr(FILE_SAVE_FAIL);
		return;
	}
	
	Stack* tmp = top;
	if (tmp == NULL) {
		RiseErr(STACK_UNDERFLOW);
		return;
	}

	while (tmp != NULL) {
		Student* pStudent = (Student*)tmp->pData;
		
		fwrite(pStudent->name, sizeof(char), pStudent->len, file);
		fwrite(&(pStudent->year), sizeof(int), 1, file);
		fwrite(&(pStudent->course), sizeof(FIELD_OF_STUDY), 1, file);
		fwrite(&(pStudent->len), sizeof(size_t), 1, file);
		tmp = tmp->next;
	}
	fclose(file);
}

void StackLoad(const char* filename) {
	FILE* file = fopen(filename, "rb");
	if (!file) {
		RiseErr(FILE_LOAD_FAIL);
		return;
	}

	if (fseek(file, 0, SEEK_END) != 0) {
		RiseErr(FILE_LOAD_FAIL);
		fclose(file);
		return;
	}

	int fileSize = ftell(file);
	int recordSize = 0;

	Student* pStudent = NULL;
	
	while (fileSize > 0) {
		size_t nameSize = 0;
		if (fseek(file, -(int)sizeof(size_t), SEEK_CUR) != 0) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent);
			return;
		}
		if (fread(&nameSize, sizeof(size_t), 1, file) != 1) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent);
			return;
		}

		int recordSize = nameSize + sizeof(int) + sizeof(FIELD_OF_STUDY) + sizeof(size_t);
		if (fseek(file, -recordSize, SEEK_CUR) != 0) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent);
			return;
		}

		pStudent = (Student*)malloc(sizeof(Student));
		pStudent->name = (char*)malloc(nameSize + 1);
		if (pStudent == NULL || pStudent->name == NULL) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent);
			return;
		}

		if (fread(pStudent->name, sizeof(char), nameSize, file) != nameSize) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent->name);
			free(pStudent);
			return;
		}

		pStudent->name[nameSize] = '\0';

		if (fread(&(pStudent->year), sizeof(int), 1, file) != 1) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent->name);
			free(pStudent);
			return;
		}

		if (fread(&(pStudent->course), sizeof(FIELD_OF_STUDY), 1, file) != 1) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent->name);
			free(pStudent);
			return;
		}

		if (fread(&(pStudent->len), sizeof(size_t), 1, file) != 1) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent->name);
			free(pStudent);
			return;
		}
		if (fseek(file, -recordSize, SEEK_CUR) != 0) {
			RiseErr(FILE_LOAD_FAIL);
			fclose(file);
			free(pStudent);
			return;
		}
		StackPush(pStudent);
		fileSize -= recordSize;
	}
	
	fclose(file);
}