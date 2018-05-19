/*
	progress.c	WJ118
*/

#include "progress.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>

static unsigned long FPS_RATE = 4UL;
static unsigned long CLOCKS_PER_MSEC = (unsigned long)CLOCKS_PER_SEC / 1000UL;


void progress_init(ProgressMeter *m, ProgressMeterType t) {
	assert(t >= PROGRESS_BAR && t <= PROGRESS_SPINNER);
	memset(m, 0, sizeof(ProgressMeter));
	m->type = t;
}

static void progress_show_bar(ProgressMeter *m) {
	/* TODO implement this */
	;
}

static void progress_show_percent(ProgressMeter *m) {
	float one_percent = 100.0f / (float)m->max_value;
	int value = m->value;
	if (value > m->max_value) {
		value = m->max_value;
	}
	int percent = (int)((float)value * one_percent + 0.5f);
	if (percent > 100) {
		percent = 100;
	}
	printf("%3d%%", percent);
	fflush(stdout);
}

static void progress_show_spinner(ProgressMeter *m) {
	/* TODO implement this */
	;
}

static void progress_update_bar(ProgressMeter *m) {
	/* TODO implement this */
	;
}

static void progress_update_percent(ProgressMeter *m) {
	printf("\b\b\b\b");

	progress_show_percent(m);
}

static void progress_update_spinner(ProgressMeter *m) {
	/* TODO implement this */
	;
}

static void progress_finish_bar(ProgressMeter *m) {
	/* TODO implement this */
	;
}

static void progress_finish_percent(ProgressMeter *m) {
	/* show 100% */
	m->value = m->max_value;
	progress_update_percent(m);
	printf("\n");
}

static void progress_finish_spinner(ProgressMeter *m) {
	/* TODO implement this */
	;
}

void progress_show(ProgressMeter *m) {
	if (m->label != NULL) {
		printf("%s ", m->label);
	}

	switch(m->type) {
		case PROGRESS_BAR:
			progress_show_bar(m);
			break;

		case PROGRESS_PERCENT:
			progress_show_percent(m);
			break;

		case PROGRESS_SPINNER:
			progress_show_spinner(m);
			break;

		default:
			assert(0);
	}

	m->timestamp = clock();
}

void progress_update(ProgressMeter *m, int value) {
	m->value = value;

	clock_t curr_timestamp = clock();
	if (curr_timestamp <= m->timestamp) {
		return;
	}

	unsigned long diff = curr_timestamp - m->timestamp;
	unsigned long fps = CLOCKS_PER_MSEC / FPS_RATE;
	if (diff < fps) {
		return;
	}
	m->timestamp = curr_timestamp;

	switch(m->type) {
		case PROGRESS_BAR:
			progress_update_bar(m);
			break;

		case PROGRESS_PERCENT:
			progress_update_percent(m);
			break;

		case PROGRESS_SPINNER:
			progress_update_spinner(m);
			break;

		default:
			assert(0);
	}
}

void progress_finish(ProgressMeter *m) {
	switch(m->type) {
		case PROGRESS_BAR:
			progress_finish_bar(m);
			break;

		case PROGRESS_PERCENT:
			progress_finish_percent(m);
			break;

		case PROGRESS_SPINNER:
			progress_finish_spinner(m);
			break;

		default:
			assert(0);
	}
}

#ifdef TEST_PROGRESS

void test_progress_percent(void) {
	int value = 0, max_value = 1024;
	ProgressMeter m;

	progress_init(&m, PROGRESS_PERCENT);
	m.label = "processing";
	m.value = value;
	m.max_value = max_value;

	progress_show(&m);

	while(value < max_value) {
		value += 5;
		usleep(10000UL);
		progress_update(&m, value);
	}
	progress_finish(&m);
}


int main(void) {
	test_progress_percent();
	return 0;
}

#endif	/* TEST */

/* EOB */
