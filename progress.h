/*
	progress.h	WJ118

	* written by Walter de Jong <walter@heiho.net>
	* This is free and unencumbered software released into the public domain.
	  Please refer to http://unlicense.org/
*/

#ifndef PROGRESS_H_WJ118
#define PROGRESS_H_WJ118	1

#include <time.h>

#define PROGRESS_LINEBUF	64

typedef enum {
	PROGRESS_BAR = 0,
	PROGRESS_PERCENT,
	PROGRESS_SPINNER
} ProgressMeterType;

typedef struct {
	ProgressMeterType type;
	char *label, *rlabel;
	int value, max_value;
	clock_t timestamp;
	char line[PROGRESS_LINEBUF];
} ProgressMeter;

void progress_init(ProgressMeter *, ProgressMeterType);
void progress_show(ProgressMeter *);
void progress_update(ProgressMeter *, int);
void progress_finish(ProgressMeter *);

#endif	/* PROGRESS_H_WJ118 */

/* EOB */

