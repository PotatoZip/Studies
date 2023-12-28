#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int myPow(int n, int exp) {
    int result = 1;
    for(; exp > 0; exp--)
        result *=n;
    return result;
}

int first_check(int a, int d, int num) {
        if(( myPow(a,d) % num) != 1) {
                return 1;
        }
        return 0;
}

int second_check(int a, int d, int num, int s) {
        for(int r = 0; r <= (s - 1); r++) {
                if(( myPow(a,d*myPow(2,r))) % num == (num - 1)) {
                        return 0;
                }
        }
        return 1;
}

int main() {
        srand(time(NULL));
        int num, k;
        printf("Enter value to check\n");
        scanf("%d", &num);
        printf("Enter k parameter\n");
        scanf("%d", &k);
        int max_division_of_2 = 2, s = 1;
        while(1) {
                if((num-1)%max_division_of_2 == 0) {
                        max_division_of_2 *= 2;
                        s++;
                        continue;
                }
                s--;
                max_division_of_2 /= 2;
                break;
        }
        int d = (num-1)/max_division_of_2;
        printf("max power of 2: %d\ns: %d\nd: %d\n", max_division_of_2, s, d);
        for(int i = 0; i < k; i++) {
                int a = rand() % num;
                printf("a: %d\n", a);
                if(first_check(a,d,num) == 1) {
                        if(second_check(a,d,num,s) == 1) {
                                printf("This value is not prime\n");
                                return 0;
                        }
                }
        }
        printf("This value is propably prime\n");


        return 0;
}

