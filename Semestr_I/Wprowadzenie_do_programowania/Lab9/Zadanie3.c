#include <stdio.h>

int main() {
	int max;
	printf("Enter max value\n");
	scanf("%d", &max);
	int arr[max];
	for(int i = 0; i < max; i++)
		arr[i] = i;
	printf("Prime numbers up to max value\n");
	for(int i = 2; i < max; i++) {
		if(arr[i] == 2 || arr[i] == 3 || arr[i] == 5 || arr[i] ==7) {
			printf("%d\n", arr[i]);
		}
		else if((arr[i]%2 != 0) && (arr[i]%3 != 0) && (arr[i]%5 != 0) && (arr[i]%7 != 0)) {
			printf("%d\n", arr[i]);
		}
	}
	return 0;
}
