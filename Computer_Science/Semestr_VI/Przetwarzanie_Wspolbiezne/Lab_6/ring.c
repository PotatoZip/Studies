#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

int main(int argc, char **argv) {
    int rank, size;
    int number, received_number;
    int next_rank, prev_rank;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size < 2) {
        if (rank == 0) {
            fprintf(stderr, "Błąd: Ten program wymaga co najmniej 2 procesów do utworzenia pierścienia.\n");
        }
        MPI_Finalize();
        return 1;
    }

    next_rank = (rank + 1) % size;
    prev_rank = (rank - 1 + size) % size;

    while (1) {

        if (rank == 0) {
            printf("Podaj liczbę (ujemna kończy):\n");
            fflush(stdout);
            if (scanf("%d", &number) != 1) {
                 number = -1;
            }
        }

        MPI_Bcast(&number, 1, MPI_INT, 0, MPI_COMM_WORLD);

        if (number < 0) {
            break;
        }

        if (rank == 0) {
            MPI_Send(&number, 1, MPI_INT, next_rank, 0, MPI_COMM_WORLD);
            MPI_Recv(&received_number, 1, MPI_INT, prev_rank, 0, MPI_COMM_WORLD, &status);
            printf("Proces %d dostal %d od procesu %d\n", rank, received_number, status.MPI_SOURCE);
            fflush(stdout);
        } else {
            MPI_Recv(&received_number, 1, MPI_INT, prev_rank, 0, MPI_COMM_WORLD, &status);
            printf("Proces %d dostal %d od procesu %d\n", rank, received_number, status.MPI_SOURCE);
            fflush(stdout);
            MPI_Send(&received_number, 1, MPI_INT, next_rank, 0, MPI_COMM_WORLD);
        }
        MPI_Barrier(MPI_COMM_WORLD);

    }

    MPI_Finalize();
    return 0;
}