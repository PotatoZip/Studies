#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/wait.h>

int main() {

	struct tm *wczas;
	time_t czas = 0;
	char bufor[1024];
	int rok = 0;

	int pdesk[2];
	time_t seconds = 0;
	pipe(pdesk);

	switch (fork()) {
	case -1:
		printf("Blad fork1\n");
		exit(1);
	case 0:
		if (mkfifo("FIFO", 0777) == -1) {
			printf("Blad mkfifo\n");
			exit(1);
		};

		switch (fork()) {
		case -1:
			printf("Blad fork2\n");
			exit(1);
		case 0:
			close(pdesk[0]);
			printf("Wczytaj liczbe sekund:\n");
			scanf("%ld", &seconds);
			write(pdesk[1], &seconds, sizeof(seconds));
			close(pdesk[1]);
			exit(0);
		}

		close(pdesk[1]);
		read(pdesk[0], &seconds, sizeof(seconds));
		czas = seconds;
		wczas=gmtime(&czas);

		write(pdesk[1], &(wczas->tm_year), sizeof(wczas->tm_year));
        write(pdesk[1], &(wczas->tm_mon), sizeof(wczas->tm_mon));
    	write(pdesk[1], &(wczas->tm_mday), sizeof(wczas->tm_mday));
        write(pdesk[1], &(wczas->tm_hour), sizeof(wczas->tm_hour));
        write(pdesk[1], &(wczas->tm_min), sizeof(wczas->tm_min));
        write(pdesk[1], &(wczas->tm_sec), sizeof(wczas->tm_sec));
		strftime(bufor,1024,"%Y-%m-%d:%T",wczas);
		printf("czas %ld to: %s\n", czas, bufor);
		printf("-Miesiac: %d\n", wczas->tm_mon + 1);
        printf("-Dzien: %d\n", wczas->tm_mday);
        printf("-Dzien tygodnia: %d\n", wczas->tm_wday);
        printf("-Rok: %d\n", wczas->tm_year);

		close(pdesk[1]);
		exit(0);

	default:

		wait(NULL);
		rok = 1900 + wczas->tm_year;
		printf("Rok: %d, %d\n", rok, wczas->year);

		break;
	}

	return 0;
}
