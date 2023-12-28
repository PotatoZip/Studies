#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void printProc() {
	printf("PID: %d\n", getpid());
	printf("PPID: %d\n", getppid());
	printf("UID: %d\n", getuid());
	printf("GID: %d\n", getuid());
}

int main() {
	int child;
	char komenda[128];
	int pid = getpid();
	sprintf(komenda, "pstree -np %d", pid);
	for (int i = 0; i < 3; i++) {
		child = fork();
		if (child == 0) {
			printf("Proces potomny %d:\n", i + 1);
			printProc();
		}
		else if (child == -1) {
			printf("Blad polecenia fork()\n");
		}
	}
	//wyswietla drzewo procesow
	if (getpid() == pid) {
		system(komenda);
	}
	//pozwala poczekac na wykonanie polecenia 
	sleep(1);

	return 0;
}

/*Liczenie procesow:
Na poczatku mamy 1 proces
przy pierwszym fork() tworzymy 1 nowy czyli mamy juz 2 (1 rodzic + 1 dziecko)
przy drugim fork() tworzymy 2 nowe czyli mamy juz 4 (1 rodzic + 3 dzieci)
przy ostatnim fork() tworzymy 4 nowe czyli mamy juz 8 (1 rodzic + 7 dzieci)
Lacznie 8 procesow
*/
