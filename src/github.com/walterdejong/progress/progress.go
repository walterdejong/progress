//
//	progress.go	WJ118
//

package progress

import (
	"fmt"
	"strings"
	"time"
)

const (
	refresh     = 250 * time.Millisecond
	spinnerText = "|/-\\"
	barWidth = 10
)

type Meter struct {
	Value, MaxValue int
	Label           string
	Timestamp       time.Time
	visible         bool
}

type Bar struct {
	Meter

	Width int
}

type Spinner struct {
	Meter
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
	m.Timestamp = time.Now()
	if m.visible {
		return
	}
	if m.Label != "" {
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

func (b *Bar) Show() {
	b.Meter.Show()

	if b.Width <= 0 {
		b.Width = barWidth
	}

	one_unit := float32(b.Width) / float32(b.MaxValue)
	value := b.Value
	if value > b.MaxValue {
		value = b.MaxValue
	}

	units := int(float32(value) * one_unit + 0.5)

	bar := "|" + strings.Repeat("=", units) + strings.Repeat(" ", b.Width - units) + "|"
	fmt.Printf("%s ", bar)
}

func (b *Bar) Update(value int) {
	b.Value = value
	if !b.shouldRefresh() {
		return
	}

	bar := strings.Repeat("\b", b.Width + 3)
	fmt.Printf("%s", bar)
	b.Show()
}

func (b *Bar) Finish() {
	// show 100%
	b.Value = b.MaxValue
	b.Update(b.Value)

	b.Meter.Finish()
}

func (s *Spinner) Show() {
	s.Meter.Show()

	s.Value++
	if s.Value >= 4 {
		s.Value = 0
	}

	fmt.Printf("%c ", spinnerText[s.Value])
}

func (s *Spinner) Update(value int) {
	// s.Value = value
	if !s.shouldRefresh() {
		return
	}
	fmt.Printf("\b\b")
	s.Show()
}

func (s *Spinner) Finish() {
	fmt.Printf("\b\b  \b\b")
	s.Meter.Finish()
}

func (p *Percent) Show() {
	p.Meter.Show()
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
	if !p.shouldRefresh() {
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
