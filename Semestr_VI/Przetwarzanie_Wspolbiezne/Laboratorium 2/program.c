#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    printf("Wiktor Zmiendak %ld\n", (long)getpid());

    return 0;
}