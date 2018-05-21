//
//	test_progress.go	WJ118
//

package main

import (
	"github.com/walterdejong/progress"
	"time"
)


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
	test_progress_percent()
}

// EOB
