all: sort
sort: Main.o Algorithms.o
	gcc -o sort Main.o Algorithms.o
Main.o: Main.c Algorithms.c Algorithms.h
	gcc -c Main.c
Algorithms.o: Algorithms.c Algorithms.h
	gcc -c Algorithms.c
clean:
	rm *.o