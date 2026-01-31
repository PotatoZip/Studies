#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
int main()

{
char buf[1024];
FILE* str=popen("cat p*.c","r");
fread(buf,1,1024,str);
printf("przeczytane:\n %s\n",buf);

pclose(str);

}
