#include <stdio.h>
#include <unistd.h>

int main()

{
FILE* str=popen("sort","w");
fprintf(str, "Ala\n");
fprintf(str, "Ania\n");
fprintf(str, "As\n");
fprintf(str, "Kasia\n");
fprintf(str, "Ula\n");
fprintf(str, "Asia\n");
fprintf(str, "Miko\n");
pclose(str);

}
