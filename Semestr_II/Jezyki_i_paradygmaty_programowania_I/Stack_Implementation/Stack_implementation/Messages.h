#pragma once

enum messages {
	ALLOC_ERR,
	FILE_SAVE_FAIL,
	FILE_LOAD_FAIL,
	STACK_UNDERFLOW
};

void RiseErr(messages mess);