#include <stdio.h>
#include <omp.h>

// ZADANIE 2
void testVariableSharing() {
    int a;
    printf("==== TEST ZMIENNYCH WSPÓŁDZIELONYCH ====\n");

    // SHARED
    a = 7;
    printf("[Shared]\n");
    #pragma omp parallel for num_threads(7) shared(a)
        for (int i = 0; i < 10; i++) {
            printf("Thread %d a=%d\n", omp_get_thread_num(), a);
            a++;
        }
    printf("Po bloku shared, a = %d\n", a);

    // PRIVATE
    a = 7;
    printf("\n[Private]\n");
    #pragma omp parallel for num_threads(7) private(a)
        for (int i = 0; i < 10; i++) {
            printf("Thread %d a=%d\n", omp_get_thread_num(), a);
            a++;
        }
    printf("Po bloku private, a = %d\n", a);

    // FIRSTPRIVATE
    a = 7;
    printf("\n[Firstprivate]\n");
    #pragma omp parallel for num_threads(7) firstprivate(a)
        for (int i = 0; i < 10; i++) {
            printf("Thread %d a=%d\n", omp_get_thread_num(), a);
            a++;
        }
    printf("Po bloku firstprivate, a = %d\n", a);
}

// ZADANIE 3
void testScheduling() {
    printf("\n==== STRATEGIE PRZYDZIAŁU ITERACJI ====\n");

    omp_sched_t strategies[] = {omp_sched_static, omp_sched_static, omp_sched_dynamic, omp_sched_dynamic};
    int chunks[] = {3, 0, 3, 0};
    const char* names[] = {
        "static, chunk=3",
        "static, default",
        "dynamic, chunk=3",
        "dynamic, default"
    };

    for (int s = 0; s < 4; s++) {
        omp_set_schedule(strategies[s], chunks[s]);
        printf("\n[%s]\n", names[s]);

        // ZADANIE 4 (MIERZENIE CZASU)
        double start = omp_get_wtime();
        #pragma omp parallel for schedule(runtime) num_threads(4)
        for (int i = 0; i < 100; i++) {
            // printf("Thread %d -> iteracja %d\n", omp_get_thread_num(), i);
            omp_get_thread_num();
        }
        double end = omp_get_wtime();
        printf("Czas: %.6f s\n", end - start);

        #pragma omp parallel for schedule(runtime) num_threads(4)
        for (int i = 0; i < 100000; i++) {
            // printf("Thread %d -> iteracja %d\n", omp_get_thread_num(), i);
            omp_get_thread_num();
        }
        end = omp_get_wtime();
        printf("Czas: %.6f s\n", end - start);
    }
}

// ZADANIE 5 i 6
void testSumStrategies() {
    printf("\n==== SUMOWANIE KWADRATÓW od 1 do 500 ====\n");
    int N = 500;
    int sum;

    // REDUCTION
    sum = 0;
    double start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum)
    for (int i = 1; i <= N; i++) {
        sum += i * i;
    }
    double end = omp_get_wtime();
    printf("[Reduction] Suma = %d, Czas: %.6f s\n", sum, end - start);

    // CRITICAL
    sum = 0;
    start = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 1; i <= N; i++) {
        int tmp = i * i;
        #pragma omp critical
        {
            sum += tmp;
        }
    }
    end = omp_get_wtime();
    printf("[Critical] Suma = %d, Czas: %.6f s\n", sum, end - start);

    // LOCK
    omp_lock_t lock;
    omp_init_lock(&lock);
    sum = 0;
    start = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 1; i <= N; i++) {
        int tmp = i * i;
        omp_set_lock(&lock);
        sum += tmp;
        omp_unset_lock(&lock);
    }
    end = omp_get_wtime();
    omp_destroy_lock(&lock);
    printf("[Lock] Suma = %d, Czas: %.6f s\n", sum, end - start);
}

int main() {
    testVariableSharing();
    testScheduling();
    testSumStrategies();

    return 0;
}
