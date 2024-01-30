#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/wait.h>

int main() {
	//Tworze potok nienazwany
	int pdesk[2];
	pipe(pdesk);

	//Potrzebne zmienne
	int fifo1, fifo2;
	int year, year1;
	char bufor[1024];

	struct tm *tm_czas;
	time_t czas1, czas2;

	//Wypisuje aktualny czas w sekundach
	time(&czas1);
	printf("Biezacy czas: %ld\n", czas1);

	switch (fork()) {
		case -1:
			printf("Blad fork1\n");
			exit(1);
		case 0:
			//Tworze potok nazwany
			if (mkfifo("FIFO", 0777) == -1) {
				printf("Blad mkfifo\n");
				exit(1);
			}

			switch (fork()) {
				case -1:
					printf("Blad fork2\n");
					exit(1);
				case 0:
					//Wczytuje z klawiatury liczbe sekund
					printf("Wczytaj liczbe sekund:\n");
					scanf("%ld", &czas1);

					//Otwieram fifo do zapisu
					fifo1 = open("FIFO", O_WRONLY);
					write(fifo1, &czas1, sizeof(czas1));
					close(fifo1);
					exit(1);
				default:
					//Otwieram fifo do odczytu
					fifo2 = open("FIFO", O_RDONLY);
					read(fifo2, &czas2, sizeof(czas2));
					printf("Odczytany czas z FIFO: %ld\n", czas2);

					//Obliczam czas na podstawie sekund
					tm_czas = localtime(&czas2);
					strftime(bufor,1024,"%Y-%m-%d:%T",tm_czas);
					printf("czas %ld to: %s\n", czas2, bufor);
					printf("Miesiac = %d\nDzien = %d\nDzien Tygodnia = %d\nRok = %d\n", (tm_czas->tm_mon) + 1, tm_czas->tm_mday, (tm_czas->tm_wday) + 1, tm_czas->tm_year + 1900);

					//Zapisuje rok do potoku nienazwanego
					year1 = tm_czas->tm_year;
					write(pdesk[1], &year1, sizeof(year1));
					close(fifo2);
			}
			exit(1);
		default:
			//Czekam na zakonczenie procesu potomnego
			wait(NULL);

			//Odczytuje rok z potoku nienazwanego
			read(pdesk[0], &year1, sizeof(int));
			printf("Zawartosc potoku: %ld\n", year1+1900);

			//Usuwam potok nazwany
			unlink("FIFO");
			close(pdesk[0]);
			close(pdesk[1]);
	}
	return 0;
}
