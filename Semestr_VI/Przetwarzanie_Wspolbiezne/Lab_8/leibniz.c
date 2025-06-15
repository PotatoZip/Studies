#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char* argv[]) {
    long long max_n;
    int num_procs, rank;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0) {
        if (argc < 2) {
            fprintf(stderr, "Please enter the number of components\n");
            max_n = -1;
        } else {
            char *endptr;
            max_n = strtoll(argv[1], &endptr, 10);

            if (*endptr != '\0' || max_n <= 0) {
                fprintf(stderr, "The number of components must be positive\n", argv[1]);
                max_n = -1;
            }
        }

        if (max_n == -1) {
             MPI_Abort(MPI_COMM_WORLD, 1);
        }
    }

    MPI_Bcast(&max_n, 1, MPI_LONG_LONG, 0, MPI_COMM_WORLD);

    if (max_n == -1) {
        MPI_Finalize();
        return 1;
    }

    double sum = 0.0;
    for (long long n = rank; n < max_n; n += num_procs) {
        double tmp = 1.0 / (2.0 * (double)n + 1.0);
        if (n % 2 == 0) {
            sum += tmp;
        } else {
            sum -= tmp;
        }
    }

    double global_sum;
    MPI_Reduce(&sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Elements count: %lld\n", max_n);
        printf("Threads count: %d\n", num_procs);
        printf("Pi approximation: %.15f\n", 4.0 * global_sum);
    }

    MPI_Finalize();
    return 0;
}