#include <stdio.h>

int which_prime(int s, int* word) {

    int prime_numbers[5] = {127, 131, 137, 139, 149};
    for(int i = 0; i < 5; i++) {
        for(int j = 0; j < s; j++) {
            if(word[j]%prime_numbers[i] < (int) 'A' || word[j]%prime_numbers[i] > (int) 'Z') {
                break;
            }
            if(j == 4) {
                return prime_numbers[i];
            }
        } 
    }
    return 0;
}

int main() {

    int t, s, letter_value, word[100];
    printf("Enter series count:\n");
    scanf("%d", &t);
    for(int i = 0; i < t; i++) {
        printf("Enter letters count in this series:\n");
        scanf("%d", &s);
        for(int j = 0; j < s; j++) {
            printf("Enter three number code:\n");
            scanf("%d", &word[j]);   
        }
        if(which_prime(s,word) == 0) {
            printf("NIECZYTELNE\n");
            continue;
        }
        printf("%d ", which_prime(s, word));
        for(int j = 0; j < s; j++) {
            char chr = word[j]%which_prime(s,word);
            printf("%c", chr);
        }
        printf("\n");
    }

    return 0;
}