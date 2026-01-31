#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Messages.h"
#include "Stack.h"

static const char* messagesErr[] = {
	"Error with memory allocation",
	"File saving error",
	"File loading error",
	"Stack underflow"
};

void RiseErr(messages mess) {
	puts(messagesErr[mess]);

	if (messagesErr[mess][0] == 'E') {
		StackFree();
		system("pause");
	}
	return;
}