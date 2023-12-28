#include <stdio.h>
#include <math.h>


int main() {
	int x;
	printf("Enter value\n");
	scanf("%d", &x);
	int size = log10(x) + 1;
	int arr[size];
	for(int i = 0; i < size; i++) {
		arr[i] = x % 10;
		x /= 10;
	}
	for(int j = 0; j < size /2 ; j++) {
		if(arr[j] == arr[size - 1 - j])
			continue;
		printf("Value is not a palindrom\n");
		return 0;
	}
	printf("Value is a palindrom\n");

	return 0;
}
