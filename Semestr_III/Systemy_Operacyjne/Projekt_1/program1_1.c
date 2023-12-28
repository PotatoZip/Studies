#include <stdio.h>
#include <unistd.h>

int main() {
	printf("----Procesy----\n");
	printf("PID: %d\n", getpid());
	printf("PPID: %d\n", getppid());
	printf("UID: %d\n", getuid());
	printf("GID: %d\n", getgid());
	printf("---------------\n");

	return 0;
}
