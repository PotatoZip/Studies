#include "Algorithms.h"

void insert_sort(int *tab, int n) {
    int j, x;
    for(int i = 1; i < n; i++) {
        x = tab[i];
        j = i - 1;
        while (tab[j] > x && j >= 0) {
            tab[j + 1] = tab[j];
            j--;
        }
        tab[j + 1] = x;
    }
}

void selection_sort(int *tab, int n) {
    int i, j, min_id, tmp;
    for (i = 0; i < n - 1; i++) {
        min_id = i;
        for (j = i + 1; j < n; j++) {
            if (tab[j] < tab[min_id]) {
                min_id = j;
            }
        }
        tmp = tab[i];
        tab[i] = tab[min_id];
        tab[min_id] = tmp;
    }
}

void bubble_sort(int *tab, int n) {
    int i, j, tmp;
    for(j = 0; j < n - 1; j++) {
        for(i = n - 2; i >= j; i--) {
            if(tab[i] > tab[i + 1]) {
                tmp = tab[i];
                tab[i] = tab[i + 1];
                tab[i + 1] = tmp;
            }
        }
    }
}

void quick_sort(int *tab, int p, int n) {
    int i = p, j = n, s, tmp;
    s = tab[(i+j)/2];
    do {
        while(tab[i] < s) {
            i++;
        }
        while(tab[j] > s) {
            j--;
        }
        if(i <= j) {
            tmp = tab[i];
            tab[i] = tab[j];
            tab[j] = tmp;
            i++;
            j--;
        }
    } while(i <= j);
   
    if(j > p) {
        quick_sort(tab, p, j);
    }
    if(i < n) {
        quick_sort(tab, i, n);
    }
}

void shell_sort(int *tab, int n) {
    int step, i, j;

	for (step = n / 2; step > 0; step /= 2) {
		for (i = step; i < n; i++) {
			int tmp = tab[i];

			for (j = i; j >= step && tab[j - step] > tmp; j -= step) {
                tab[j] = tab[j - step];
            }
			tab[j] = tmp;
		}
	}
}

void heap_sort(int* tab, int n)
{
	for (int i = n / 2 - 1; i >= 0; i--)
		heapify(tab, n, i);

	for (int i = n - 1; i > 0; i--) 
	{
		int tmp = tab[0];
        tab[0] = tab[i];
        tab[i] = tmp;
		heapify(tab, i, 0);
	}
}

void heapify(int *tab, int n, int i) {
    int largest = i;
	int left = 2 * i + 1;
	int right = 2 * i + 2;

	if (left < n && tab[left] > tab[largest]) {
   		largest = left;
    }

	if (right < n && tab[right] > tab[largest]) {
        largest = right;
    }

	if (largest != i) {
		int tmp = tab[i];
        tab[i] = tab[largest];
        tab[largest] = tmp;
		heapify(tab, n, largest);
	}
}