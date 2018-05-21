/*
	test_progress.go	WJ118

	* written by Walter de Jong <walter@heiho.net>
	* This is free and unencumbered software released into the public domain.
	  Please refer to http://unlicense.org/
*/

package main

import (
	"github.com/walterdejong/progress"
	"time"
)

func test_progress_bar() {
	max_value := 1024
	p := progress.Bar{Width: 20}
	p.Label = "downloading"
	p.MaxValue = max_value
	p.Show()

	value := 0
	for value < max_value {
		value += 15
		time.Sleep(100 * time.Millisecond)
		p.Update(value)
	}
	p.Finish()
}

func test_progress_spinner() {
	p := progress.Spinner{}
	p.Label = "busy"
	p.Show()

	value := 0
	max_value := 1024
	for value < max_value {
		value += 15
		time.Sleep(100 * time.Millisecond)
		p.Update(0)
	}
	p.Finish()
}

func test_progress_percent() {
	max_value := 1024
	p := progress.Percent{}
	p.Label = "processing"
	p.MaxValue = max_value
	p.Show()

	value := 0
	for value < max_value {
		value += 15
		time.Sleep(100 * time.Millisecond)
		p.Update(value)
	}
	p.Finish()
}

func main() {
	test_progress_bar()
	test_progress_spinner()
	test_progress_percent()
}

// EOB
