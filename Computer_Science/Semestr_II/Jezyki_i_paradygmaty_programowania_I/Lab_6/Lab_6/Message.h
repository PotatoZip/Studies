#pragma once

enum MESSAGES {
	MEMORY_ALLOCATION_ERROR,
	SAMPLE_ERROR,
	TOTAL,
};

void mess_function(enum MESSAGES mess);