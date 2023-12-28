#include <stdio.h>
#include <math.h>

int main() {

	long long int x;
	printf("Enter value:\n");
	scanf("%lld", &x);
	int size = log10(x) + 1;
	int count, arr[size], freq[size];
	for(int i = 0; i < size; i++) {
		arr[i] = x % 10;
		x /= 10;
		freq[i] = -1;
	}
	for(int j = 0; j < size; j++) {
		count = 1;
		for(int k = j + 1; k < size; k++) {
			if(arr[j] == arr[k]) {
				count += 1;
				freq[k] = 0;
			}
		}
		if(freq[j] != 0)
			freq[j] = count;
	}
	for(int z = 0; z < size; z++) {
		if(freq[z] >= 2)
			printf("Value: %d Count: %d\n", arr[z], freq[z]); 
	}
	return 0;
}
