#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

int main(int argc, char **argv) {
    int rank, size;
    int number;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    MPI_Comm_size(MPI_COMM_WORLD, &size);

    while (1) {

        if (rank == 0) {
            printf("Podaj liczbę (ujemna kończy):\n");
            fflush(stdout);
            if (scanf("%d", &number) != 1) {
                fprintf(stderr, "Błąd: Nieprawidłowe dane wejściowe. Kończenie.\n");
                number = -1;
            }
        }

        MPI_Bcast(
            &number,
            1,
            MPI_INT,
            0,
            MPI_COMM_WORLD
        );

        if (number < 0) {
            break;
        }

        printf("Proces %d otrzymal liczbe: %d\n", rank, number);
        fflush(stdout);

        MPI_Barrier(MPI_COMM_WORLD);

    }

    MPI_Finalize();

    return 0;
}