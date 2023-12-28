#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include "Student.h"
#include "Stack.h"
#include "Menu.h"
#include "Messages.h"

void Menu() {
	int ans = 0;
	StackInit(StructFree);
	while (true) {
		int tmp;
		PrintMenu();
		if (scanf_s("%d", &ans) == 1) {
			switch (ans) {
			case 1:
				ClearTerminal();
				Push();
				ClearTerminal();
				break;
			case 2:
				ClearTerminal();
				Pop();
				printf("Press any key to continue...\n");
				tmp = getch();
				ClearTerminal();
				break;
			case 3:
				ClearTerminal();
				ShowFirstElement();
				printf("Press any key to continue...\n");
				tmp = getch();
				ClearTerminal();
				break;
			case 4:
				ClearTerminal();
				Clear();
				break;
			case 5:
				ClearTerminal();
				Show();
				printf("Press any key to continue...\n");
				tmp = getch();
				ClearTerminal();
				break;
			case 6:
				ClearTerminal();
				Find();
				printf("Press any key to continue...\n");
				tmp = getch();
				ClearTerminal();
				break;
			case 7:
				ClearTerminal();
				Save();
				break;
			case 8:
				ClearTerminal();
				Load();
				break;
			case 9:
				exit(0);
				break;
			deafult:
				printf("Invalide input\n");
				break;
			};
		}
		else {
			ClearTerminal();
			printf("Invalid input\nPress any key to continue...\n");
			tmp = getch();
			ClearTerminal();
		}
		while (getchar() != '\n');
	}
}

void PrintMenu() {
	printf("============================\nStack implementation program\n============================\n\n");
	printf("Select option:\n1 -> Push to stack\n2 -> Pop from stack\n3 -> Show first element\n4 -> Clear stack\n5 -> Show stack\n6 -> Find element in stack\n7 -> Save all stack elements to binary file\n8 -> Open stack from file\n9 -> Exit\n");
}

void Push() {
	char name[512];
	int year;
	FIELD_OF_STUDY course;

	printf("Enter name:\n");
	if (scanf_s("%s", name, sizeof(name)) != 1) {
		printf("Invalid value\n");
		while(getchar() != '\n') {}
		return;
	}

	printf("Enter year:\n");
	if (scanf_s("%d", &year) != 1 || year < 0) {
		printf("Invalid value\n");
		while(getchar() != '\n') {}
		return;
	}

	printf("Enter field of study:\n0 -> Computer science\n1 -> Mathematics\n2 -> Biology\n3 -> History\n");
	if (scanf_s("%d", &course) != 1 || (course != 0 && course != 1 && course != 2 && course != 3)) {
		printf("Invalid value\n");
		while (getchar() != '\n') {}
		return;
	}
	void* ptr = StructPush(name, year, course);
	if (!StackPush(ptr)) {
		RiseErr(ALLOC_ERR);
	}
}

void Pop() {
	if (StackTop() == NULL) {
		printf("Stack is empty\n");
		return;
	}

	void *tmp = StackPop();
	if (tmp != NULL) {
		printf("Data deleted:\n\n");
		StructPrint(tmp);
	}
	StructFree(tmp);
}

void Clear() {
	StackFree();
}

void Show() {
	Stack* ptr = StackTop();
	if (!ptr) {
		printf("Stack is empty\n");
	}
	while (ptr) {
		StructPrint(ptr->pData);
		ptr = ptr->next;
	}
}

void Find() {
	char name[512];
	printf("Enter name to find:\n");
	if (scanf_s("%s", name, sizeof(name)) != 1) {
		printf("Invalid input\n");
		while(getchar() != '\n') {}
		return;
	}

	Student* pStudent = (Student*)malloc(sizeof(Student));
	if (!pStudent) {
		RiseErr(ALLOC_ERR);
		return;
	}

	memset(pStudent, 0, sizeof(Student));
	pStudent->name = (char*)malloc((strlen(name) + 1) * sizeof(char));

	if (!pStudent->name) {
		RiseErr(ALLOC_ERR);
		return;
	}
	strcpy(pStudent->name, name);
	void* ptr = StackFind(pStudent, StructFind, 1);

	if (ptr) {
		printf("Student found:\n");
		StructPrint(ptr);
	}
	else {
		printf("Student not found\n");
	}

	while (ptr) {
		ptr = StackFind(pStudent, StructFind, 0);
		if (ptr) {
			StructPrint(ptr);
		}
	}
	StructFree(ptr);
}

void Save() {
	StackSave("student_stack.bin");
}

void Load() {
	StackLoad("student_stack.bin");
}

void ShowFirstElement() {
	Stack* ptr = StackTop();
	if (ptr == NULL) {
		printf("Stack is empty\n");
	}
	else {
		StructPrint(ptr->pData);
	}
}

void ClearTerminal() {
	printf("\033[2J");
	printf("\033[H");
}