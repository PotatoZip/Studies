#include <stdio.h>

int main(){
	int arr[10], freq[10], count;
	printf("Enter 10 values to array\n");
	for(int i = 0; i < 10; i++) {
		scanf("%d", &arr[i]);
		freq[i] = -1;
	}
	for(int j = 0; j < 10 - 1; j++) {
		count = 1;
		for(int k = 1 + j; k < 10; k++) {
			if( arr[j] == arr[k]) {
				count += 1;
				freq[k] = 0;
			}
		}
		if(freq[j] != 0)
			freq[j] = count;
	}
	for(int z = 0; z < 10; z++) {
		if(freq[z] >= 2)
			printf("Value: %d Count: %d\n", arr[z], freq[z]);
	}

	return 0;
}
