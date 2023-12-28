#include <stdio.h>
#include <conio.h>
#include <string.h>

int convert_to_decimal(char ch) {
    int value = 0;
    switch(ch) {
        case 'I': value = 1; break;
        case 'V': value = 5; break;
        case 'X': value = 10; break;
        case 'L': value = 50; break;
        case 'C': value = 100; break;
        case 'D': value = 500; break;
        case 'M': value = 1000; break;
        case '\0': value = 0; break;
    }
    return value;
}

int decimal_value(char* ch) {
    int value = 0;
    for(int i = 0; i < strlen(ch); i++) {
            if(convert_to_decimal(ch[i]) >= convert_to_decimal(ch[i+1])) {
                 value += convert_to_decimal(ch[i]);
            }
            else {
                value += (convert_to_decimal(ch[i+1]) - convert_to_decimal(ch[i]));
                i++;
            }
    }
    return value;
}


int main() {
    char roman_value1[100], roman_value2[100];
    printf("Enter two values in roman system\n");
    scanf("%s %s", &roman_value1, &roman_value2);
    /*
    for(int i = 0; i < strlen(roman_value1); i++) {
        if(convert_to_decimal(roman_value1[i]) >= convert_to_decimal(roman_value1[i+1])) {
            val_decimal1 += convert_to_decimal(roman_value1[i]);
        }
        else {
            val_decimal1 += convert_to_decimal(roman_value1[i+1]) - convert_to_decimal(roman_value1[i]);
        }
    }
    */
    int val_decimal1 = decimal_value(roman_value1);
    int val_decimal2 = decimal_value(roman_value2);
    int sum = val_decimal1 + val_decimal2;
    printf("First value: %d\nSecond value: %d\n", val_decimal1, val_decimal2);
    printf("The sum of this two values is: %d\n", sum);
    getch();
    return 0;
}