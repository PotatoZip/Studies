#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "Algorithms.c"
#define PRINT

int main() {
    clock_t start_time, end_time;
    char choice;
    int n;
    srand(time(NULL));
    printf("Please select sorting algorithm:\n[i] - insert sort\n[s] - selection sort\n[b] - bubble sort\n[q] - quick sort\n[l] - shell sort\n[h] - heap sort\n");
    scanf(" %c", &choice);
    printf("Enter values count that yoqu want to sort\n");
    scanf("%d", &n);
    
    //Generate random values to file dane.txt
    FILE *input_file;
    input_file = fopen("dane.txt", "w");
    if (input_file == NULL) {
        printf("Error opening input file!\n");
        return 1;
    }
    for (int i = 0; i < n; i++) {
        int rand_num = rand() % 201 - 100;
        fprintf(input_file, "%d ", rand_num); 
    }
    fclose(input_file);

    //Create array with n random values from dane.txt
    int value;
    int* arr = (int*)malloc(n * sizeof(int));
    input_file = fopen("dane.txt", "r");
    if (input_file == NULL) {
        printf("Error opening input file!\n");
        return 1;
    }
    for(int i = 0; i < n; i++) {
        fscanf(input_file, "%d", &arr[i]);
    }
    fclose(input_file);

    //Sort array with selected algorithm
    switch (choice) {
        case 'i':
            start_time = clock();
            insert_sort(arr, n);
            end_time = clock();
            break;
        case 's':
            start_time = clock();
            selection_sort(arr, n);
            end_time = clock();
            break;
        case 'b':
            start_time = clock();
            bubble_sort(arr, n);
            end_time = clock();
            break;
        case 'q':
            start_time = clock();
            quick_sort(arr, 0, n);
            end_time = clock();
            break;
        case 'l':
            start_time = clock();
            shell_sort(arr, n);
            end_time = clock();
            break;
        case 'h':
            start_time = clock();
            heap_sort(arr, n);
            end_time = clock();
            break;
        default:
            printf("Error\n");
    }
    printf("Random values sort time: %f seconds\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);

    //Same procedure but for sorted values
    input_file = fopen("dane.txt", "w");
    if (input_file == NULL) {
        printf("Error opening input file!\n");
        return 1;
    }
    for (int i = 0; i < n; i++) {
        fprintf(input_file, "%d ", arr[i]); 
    }
    fclose(input_file);

    input_file = fopen("dane.txt", "r");
    if (input_file == NULL) {
        printf("Error opening input file!\n");
        return 1;
    }
    for(int i = 0; i < n; i++) {
        fscanf(input_file, "%d", &arr[i]);
    }
    fclose(input_file);
    
    switch (choice) {
        case 'i':
            start_time = clock();
            insert_sort(arr, n);
            end_time = clock();
            break;
        case 's':
            start_time = clock();
            selection_sort(arr, n);
            end_time = clock();
            break;
        case 'b':
            start_time = clock();
            bubble_sort(arr, n);
            end_time = clock();
            break;
        case 'q':
            start_time = clock();
            quick_sort(arr, 0, n);
            end_time = clock();
            break;
        case 'l':
            start_time = clock();
            shell_sort(arr, n);
            end_time = clock();
            break;
        case 'h':
            start_time = clock();
            heap_sort(arr, n);
            end_time = clock();
            break;
        default:
            printf("Error\n");
    }
    printf("Sorted values sort time: %f seconds\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    
    //Same procedure but for reverse sorted array
    for(int i = 0; i < n/2; i++) {
        int tmp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = tmp;
    }
    
    switch (choice) {
        case 'i':
            start_time = clock();
            insert_sort(arr, n);
            end_time = clock();
            break;
        case 's':
            start_time = clock();
            selection_sort(arr, n);
            end_time = clock();
            break;
        case 'b':
            start_time = clock();
            bubble_sort(arr, n);
            end_time = clock();
            break;
        case 'q':
            start_time = clock();
            quick_sort(arr, 0, n);
            end_time = clock();
            break;
        case 'l':
            start_time = clock();
            shell_sort(arr, n);
            end_time = clock();
            break;
        case 'h':
            start_time = clock();
            heap_sort(arr, n);
            end_time = clock();
            break;
        default:
            printf("Error\n");
    }
    printf("Reverse sorted values sort time: %f seconds\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    
    free(arr);
    return 0;
}
