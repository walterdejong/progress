/*
	progress.go	WJ118

	* written by Walter de Jong <walter@heiho.net>
	* This is free and unencumbered software released into the public domain.
	  Please refer to http://unlicense.org/
*/

package progress

import (
	"fmt"
	"strings"
	"time"
)

const (
	refresh     = 250 * time.Millisecond
	spinnerText = "|/-\\"
	barWidth    = 10
)

type Meter struct {
	Value, MaxValue int
	Label           string
	Timestamp       time.Time
	visible         bool
	line            string
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

func (m *Meter) render() {
	/*
		m.line = ...
	*/
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
		line_copy := m.line
		m.render()
		if line_copy != m.line {
			print m.line
		}
	*/
}

func (m *Meter) Finish() {
	fmt.Println("")
	m.visible = false
	m.line = ""
}

func (b *Bar) render() {
	if b.Width <= 0 {
		b.Width = barWidth
	}

	one_unit := float32(b.Width) / float32(b.MaxValue)
	value := b.Value
	if value > b.MaxValue {
		value = b.MaxValue
	}

	units := int(float32(value)*one_unit + 0.5)

	b.line = "|" + strings.Repeat("=", units) + strings.Repeat(" ", b.Width-units) + "|"
}

func (b *Bar) Show() {
	b.Meter.Show()

	b.render()
	fmt.Printf("%s ", b.line)
}

func (b *Bar) Update(value int) {
	b.Value = value
	if !b.shouldRefresh() {
		return
	}

	line_copy := b.line
	b.render()
	if line_copy == b.line {
		return
	}

	erase := strings.Repeat("\b", b.Width+3)
	fmt.Printf("%s%s ", erase, b.line)
}

func (b *Bar) Finish() {
	// show 100%
	b.Value = b.MaxValue
	b.Update(b.Value)

	b.Meter.Finish()
}

func (s *Spinner) render() {
	s.Value++
	if s.Value >= 4 {
		s.Value = 0
	}

	s.line = fmt.Sprintf("%c", spinnerText[s.Value])
}

func (s *Spinner) Show() {
	s.Meter.Show()
	s.render()
	fmt.Printf("%s ", s.line)
}

func (s *Spinner) Update(value int) {
	// s.Value = value
	if !s.shouldRefresh() {
		return
	}
	fmt.Printf("\b\b")
	s.render()
	fmt.Printf("%s ", s.line)
}

func (s *Spinner) Finish() {
	fmt.Printf("\b\b  \b\b")
	s.Meter.Finish()
}

func (p *Percent) render() {
	one_percent := 100.0 / float32(p.MaxValue)
	value := p.Value
	if value > p.MaxValue {
		value = p.MaxValue
	}
	percent := int32(float32(value)*one_percent + 0.5)
	if percent > 100 {
		percent = 100
	}
	p.line = fmt.Sprintf("%3d%%", percent)
}

func (p *Percent) Show() {
	p.Meter.Show()
	p.render()
	fmt.Printf("%s ", p.line)
}

func (p *Percent) Update(value int) {
	p.Value = value
	if !p.shouldRefresh() {
		return
	}

	line_copy := p.line
	p.render()
	if line_copy == p.line {
		return
	}

	fmt.Printf("\b\b\b\b\b%s ", p.line)
}

func (p *Percent) Finish() {
	// show 100%
	p.Value = p.MaxValue
	p.Update(p.Value)

	p.Meter.Finish()
}

// EOB
