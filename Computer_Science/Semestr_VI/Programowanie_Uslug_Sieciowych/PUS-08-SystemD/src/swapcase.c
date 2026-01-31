#include <stdio.h>
#include <ctype.h>

int main(void)
{
    int c;

    /* Czytamy do końca pliku (Ctrl‑D na UNIX‑ach lub Ctrl‑Z+Enter w Windows) */
    while ((c = getchar()) != EOF) {
        if (islower(c))
            c = toupper(c);
        else if (isupper(c))
            c = tolower(c);

        putchar(c);
        if (c == '\n')
            fflush(stdout);
    }
    return 0;
}
