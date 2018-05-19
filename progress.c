/*
	progress.c	WJ118

	* written by Walter de Jong <walter@heiho.net>
	* This is free and unencumbered software released into the public domain.
	  Please refer to http://unlicense.org/
*/

#include "progress.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>

static const unsigned long FPS_RATE = 4UL;
static const unsigned long CLOCKS_PER_MSEC = (unsigned long)CLOCKS_PER_SEC / 1000UL;

static const int BAR_WIDTH = 20;

static const char *SPIN = "|/-\\";


void progress_init(ProgressMeter *m, ProgressMeterType t) {
	assert(t >= PROGRESS_BAR && t <= PROGRESS_SPINNER);
	memset(m, 0, sizeof(ProgressMeter));
	m->type = t;
}

static void progress_show_bar(ProgressMeter *m) {
	float one_unit = (float)BAR_WIDTH / (float)m->max_value;
	int value = m->value;
	if (m->value > m->max_value) {
		value = m->max_value;
	}
	int units = (int)((float)value * one_unit + 0.5f);

	char bar[BAR_WIDTH + 3];
	bar[0] = '|';
	bar[BAR_WIDTH + 1] = '|';
	bar[BAR_WIDTH + 2] = 0;
	for(int i = 1; i < BAR_WIDTH + 1; i++) {
		if (i <= units) {
			bar[i] = '=';
		} else {
			bar[i] = ' ';
		}
	}
	printf("%s ", bar);
	fflush(stdout);
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
	m->value++;
	if (m->value >= 4) {
		m->value = 0;
	}

	printf("%c ", SPIN[m->value]);
	fflush(stdout);
}

static void progress_update_bar(ProgressMeter *m) {
	char bar[BAR_WIDTH + 4];
	memset(bar, '\b', BAR_WIDTH + 3);
	bar[BAR_WIDTH + 3] = 0;
	printf("%s", bar);

	progress_show_bar(m);
}

static void progress_update_percent(ProgressMeter *m) {
	printf("\b\b\b\b");

	progress_show_percent(m);
}

static void progress_update_spinner(ProgressMeter *m) {
	printf("\b\b");

	progress_show_spinner(m);
}

static void progress_finish_bar(ProgressMeter *m) {
	/* erase bar */
	char erase[BAR_WIDTH + 4];
	memset(erase, '\b', BAR_WIDTH + 3);
	erase[BAR_WIDTH + 3] = 0;
	printf("%s%*s\n", erase, BAR_WIDTH + 3, " ");
}

static void progress_finish_percent(ProgressMeter *m) {
	/* show 100% */
	m->value = m->max_value;
	progress_update_percent(m);
	printf("\n");
}

static void progress_finish_spinner(ProgressMeter *m) {
	printf("\b\b  \n");
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
	if (m->type != PROGRESS_SPINNER) {
		m->value = value;
	}

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

void test_progress_bar(void) {
	int value = 0, max_value = 1024;
	ProgressMeter m;

	progress_init(&m, PROGRESS_BAR);
	m.label = "downloading";
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

void test_progress_spinner(void) {
	int value = 0, max_value = 1024;
	ProgressMeter m;

	progress_init(&m, PROGRESS_SPINNER);
	m.label = "busy";

	progress_show(&m);

	while(value < max_value) {
		value += 5;
		usleep(10000UL);
		progress_update(&m, 0);
	}
	progress_finish(&m);
}

int main(void) {
	test_progress_bar();
	test_progress_spinner();
	test_progress_percent();
	return 0;
}

#endif	/* TEST */

/* EOB */
