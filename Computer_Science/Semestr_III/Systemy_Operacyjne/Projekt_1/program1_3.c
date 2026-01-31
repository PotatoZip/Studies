#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
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
			int exe = execl("/bin/echo", "echo", "Proces dziecka", NULL);
			if (exe == -1) {
				perror("Error: operacja exec() zakonczona niepowodzeniem\n");
			}
		}
		else if (child == -1) {
			perror("Error: operacja fork() zakonczona niepowodzeniem\n");
		}
	}

	for (int i = 0; i < 3; i++) {
		int info;
		int id = wait(& info);
		if (info != 0) {
			perror("Error: proces potomka zakonczony niepowodzeniem\n");
		}
		else {
			printf("Proces %d, Statut %d\n", id, info);
		}
	}

	if (getpid() == pid) {
		system(komenda);
	}

	sleep(1);

	return 0;
}

/*Liczba procesow potomnych zmniejszy sie do 3
Dodana zostala obsluga bledow
Funkcja execl zastepuje czesc procesow
Laczna liczba procesow wynosi 4
*/
