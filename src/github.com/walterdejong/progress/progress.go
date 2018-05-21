//
//	progress.go	WJ118
//

package progress

import (
	"fmt"
	"time"
)

const (
	refresh = 250 * time.Millisecond
)

type Meter struct {
	Value, MaxValue int
	Label           string
	Timestamp       time.Time
	visible			bool
}

type Percent struct {
	Meter
}

type Progresser interface {
	Show()
	Update(value int)
	Finish()
}

func (m *Meter) shouldRefresh() bool {
	// returns true if it's time to re-display the meter
	t := time.Now()
	elapsed := t.Sub(m.Timestamp)
	return elapsed >= refresh
}

func (m *Meter) Show() {
	if m.visible {
		return
	}
	if (m.Label != "") {
		fmt.Printf("%s ", m.Label)
	}
	m.visible = true
}

func (m *Meter) Update(value int) {
/*
	m.Value = value
	if ! m.shouldRefresh() {
		return
	}
	m.Show()
*/
}

func (m *Meter) Finish() {
	fmt.Println("")
	m.visible = false
}

func (p *Percent) Show() {
	p.Meter.Show()
	p.Timestamp = time.Now()
	one_percent := 100.0 / float32(p.MaxValue)
	value := p.Value
	if value > p.MaxValue {
		value = p.MaxValue
	}
	percent := int32(float32(value)*one_percent + 0.5)
	if percent > 100 {
		percent = 100
	}
	fmt.Printf("%3d%% ", percent)
}

func (p *Percent) Update(value int) {
	p.Value = value
	if ! p.shouldRefresh() {
		return
	}
	fmt.Printf("\b\b\b\b\b")
	p.Show()
}

func (p *Percent) Finish() {
	// show 100%
	p.Value = p.MaxValue
	p.Update(p.Value)

	p.Meter.Finish()
}

// EOB
