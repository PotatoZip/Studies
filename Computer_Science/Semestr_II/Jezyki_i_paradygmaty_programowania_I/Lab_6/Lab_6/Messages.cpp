#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "Message.h"

static const char* message_arr[] = {
	"E Memory allocaton error",
	"W Sample error"
};

void mess_function(enum MESSAGES mess) {
	puts(message_arr[mess] + 1);
	if (message_arr[mess][0] == 'E') {
		system("pause");
	}

	return;
}
