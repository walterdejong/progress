/*
    Progress    WJ122
    lib.rs

    * written by Walter de Jong <walter@heiho.net>
    * This is free and unencumbered software released into the public domain.
      Please refer to http://unlicense.org/
*/

use std::fmt;
use std::io::{stdout, Write};
use std::time::Instant;

struct ProgressMeter {
    label: String,
    rlabel: String,
    value: i32,
    max_value: i32,
    timestamp: Instant,
    have_vt100: bool,
}

impl ProgressMeter {
    const FPS_RATE: i32 = 4;

    fn new() -> ProgressMeter {
        let have_vt100 = ProgressMeter::determine_vt100();

        ProgressMeter {
            label: String::new(),
            rlabel: String::new(),
            value: 0,
            max_value: 0,
            timestamp: Instant::now(),
            have_vt100,
        }
    }

    fn new_meter(label: &str, rlabel: &str, max_value: i32) -> ProgressMeter {
        let have_vt100 = ProgressMeter::determine_vt100();

        ProgressMeter {
            label: label.to_owned(),
            rlabel: rlabel.to_owned(),
            value: 0,
            max_value,
            timestamp: Instant::now(),
            have_vt100,
        }
    }

    // Returns true if we have a vt100 capable terminal
    fn determine_vt100() -> bool {
        if let Ok(term) = std::env::var("TERM") {
            if term == "dumb" {
                // dumb terminal does not support ANSI escape sequences
                false
            } else {
                // any terminal other than "dumb" should be capable enough
                // for our few ANSI escape sequences
                true
            }
        } else {
            // TERM variable was not set
            false
        }
    }

    fn set_label(&mut self, label: &str) {
        self.label = label.to_owned();
    }

    fn set_rlabel(&mut self, rlabel: &str) {
        self.rlabel = rlabel.to_owned();
    }

    fn back_rlabel(&self) {
        if self.rlabel.is_empty() {
            return;
        }

        let length = self.rlabel.len() + 1;
        if self.have_vt100 {
            print!("\x1b[{}D", length);
        } else {
            // repeat character (with empty align)
            print!("{:\x08<1$}", "", length);
        }
    }

    fn erase_rlabel(&self) {
        if self.rlabel.is_empty() {
            return;
        }

        self.back_rlabel();

        if self.have_vt100 {
            print!("\x1b[K");
        } else {
            // repeat character (with empty align)
            let length = self.rlabel.len() + 1;
            print!("{: <1$}", "", length);
            self.back_rlabel();
        }
    }

    fn need_update(&mut self) -> bool {
        let t1 = Instant::now();
        let dt = t1 - self.timestamp;
        if dt.as_secs_f32() >= 1.0 / ProgressMeter::FPS_RATE as f32 {
            self.timestamp = t1;
            true
        } else {
            false
        }
    }
}

pub trait Progress {
    fn get_value(&self) -> i32;
    fn get_max_value(&self) -> i32;

    fn set_label(&mut self, label: &str);
    fn set_rlabel(&mut self, rlabel: &str);
    fn set_value(&mut self, value: i32);
    fn set_max_value(&mut self, value: i32);

    fn show(&self);
    fn hide(&self);
    fn update(&mut self, value: i32);
    fn finish(&self);

    fn update_value(&mut self, value: i32);
    fn update_display(&self);
}

pub struct ProgressBar {
    meter: ProgressMeter,
    bar_width: usize,
    cached: String,                     // cached bar presentation
}

impl fmt::Display for ProgressBar {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if ! self.meter.label.is_empty() {
            write!(f, "{} ", &self.meter.label)?;
        }

        if self.cached.is_empty() {
            write!(f, "{} ", self.make_bar())?;
        } else {
            write!(f, "{} ", self.cached)?;
        }

        if ! self.meter.rlabel.is_empty() {
            write!(f, "{} ", &self.meter.rlabel)?;
        }

        Ok(())
    }

}

impl Progress for ProgressBar {
    // TODO implement Progress for ProgressBar

    fn get_value(&self) -> i32 {
        return self.meter.value;
    }

    fn get_max_value(&self) -> i32 {
        return self.meter.max_value;
    }

    fn set_label(&mut self, label: &str) {
        self.meter.set_label(label);
    }

    fn set_rlabel(&mut self, rlabel: &str) {
        self.meter.set_rlabel(rlabel);
    }

    fn set_value(&mut self, value: i32) {
        self.meter.value = value;

        let new_bar = self.make_bar();
        if new_bar != self.cached {
            self.cached = new_bar;
        }
    }

    fn set_max_value(&mut self, value: i32) {
        self.meter.max_value = value;

        let new_bar = self.make_bar();
        if new_bar != self.cached {
            self.cached = new_bar;
        }
    }

    fn show(&self) {
        print!("{}", &self);
        stdout().flush().unwrap();
    }

    fn hide(&self) {
        if self.meter.have_vt100 {
            print!("\r\x1b[K");
        } else {
            let length = self.meter.label.len() + 1 + self.bar_width + 3 + self.meter.rlabel.len() + 1;
            print!("\r{: <1$}\r", "", length);
        }
        stdout().flush().unwrap();
    }

    fn update(&mut self, value: i32) {
        self.update_value(value);

        if self.meter.need_update() {
            let new_bar = self.make_bar();
            if new_bar != self.cached {
                self.cached = new_bar;
                self.update_display();
            }
        }
    }

    fn update_value(&mut self, value: i32) {
        self.meter.value = value;
        if self.meter.value > self.meter.max_value {
            self.meter.value = self.meter.max_value;
        }
    }

    fn update_display(&self) {
        self.meter.back_rlabel();

        print!("{:\x08<1$}", "", self.bar_width + 3);
        print!("{} ", self.cached);

        if ! self.meter.rlabel.is_empty() {
            print!("{} ", &self.meter.rlabel);
        }
        stdout().flush().unwrap();
    }

    fn finish(&self) {
        self.update_display();
        println!();
    }
}

impl ProgressBar {
    const BAR_WIDTH: usize = 20;

    pub fn new() -> ProgressBar {
        ProgressBar {
            meter: ProgressMeter::new(),
            bar_width: ProgressBar::BAR_WIDTH,
            cached: String::new(),
        }
    }

    pub fn new_bar(label: &str, rlabel: &str, max_value: i32, width: usize) -> ProgressBar {
        assert!(width > 2);
        ProgressBar {
            meter: ProgressMeter::new_meter(label, rlabel, max_value),
            bar_width: width,
            cached: String::new(),
        }
    }

    fn make_bar(&self) -> String {
        let mut buf = vec![' ' as u8; self.bar_width + 2];
        buf[0] = '|' as u8;
        buf[self.bar_width + 1] = '|' as u8;

        let one_unit = self.bar_width as f32 / self.get_max_value() as f32;
        let value = std::cmp::min(self.get_value(), self.get_max_value());
        let units = (value as f32 * one_unit + 0.5) as usize;

        for i in 0..self.bar_width {
            if i < units {
                buf[i + 1] = '=' as u8;
            } else {
                break;
            }
        }
        String::from_utf8(buf).unwrap()
    }
}

pub struct ProgressPercent {
    meter: ProgressMeter,
}

impl fmt::Display for ProgressPercent {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if ! self.meter.label.is_empty() {
            write!(f, "{} ", &self.meter.label)?;
        }

        write!(f, "{:3}% ", self.calc_percentage())?;

        if ! self.meter.rlabel.is_empty() {
            write!(f, "{} ", &self.meter.rlabel)?;
        }

        Ok(())
    }
}

impl Progress for ProgressPercent {
    fn get_value(&self) -> i32 {
        return self.meter.value;
    }

    fn get_max_value(&self) -> i32 {
        return self.meter.max_value;
    }

    fn set_label(&mut self, label: &str) {
        self.meter.set_label(label);
    }

    fn set_rlabel(&mut self, rlabel: &str) {
        self.meter.set_rlabel(rlabel);
    }

    fn set_value(&mut self, value: i32) {
        self.meter.value = value;
    }

    fn set_max_value(&mut self, value: i32) {
        self.meter.max_value = value;
    }

    fn show(&self) {
        print!("{}", &self);
        stdout().flush().unwrap();
    }

    fn hide(&self) {
        if self.meter.have_vt100 {
            print!("\r\x1b[K");
        } else {
            let length = 5 + self.meter.label.len() + 1 + self.meter.rlabel.len() + 1;
            print!("\r{: <1$}\r", "", length);
        }
        stdout().flush().unwrap();
    }

    fn update(&mut self, value: i32) {
        let old_percent = self.calc_percentage();

        self.update_value(value);

        let new_percent = self.calc_percentage();

        if new_percent != old_percent && self.meter.need_update() {
            self.update_display();
        }
    }

    fn update_value(&mut self, value: i32) {
        self.meter.value = value;
        if self.meter.value > self.meter.max_value {
            self.meter.value = self.meter.max_value;
        }
    }

    fn update_display(&self) {
        self.meter.back_rlabel();

        print!("\x08\x08\x08\x08\x08{:3}% ", self.calc_percentage());

        if ! self.meter.rlabel.is_empty() {
            print!("{} ", &self.meter.rlabel);
        }
        stdout().flush().unwrap();
    }

    fn finish(&self) {
        self.update_display();
        println!();
    }
}

impl ProgressPercent {
    pub fn new() -> ProgressPercent {
        ProgressPercent {
            meter: ProgressMeter::new(),
        }
    }

    pub fn new_percent(label: &str, rlabel: &str, max_value: i32) -> ProgressPercent {
        ProgressPercent {
            meter: ProgressMeter::new_meter(label, rlabel, max_value),
        }
    }

    fn calc_percentage(&self) -> i32 {
        let mut percent: i32;
        if self.meter.max_value == 0 {
            // prevent div by zero
            percent = 0;
        } else {
            percent = (100.0 / self.meter.max_value as f32 * self.meter.value as f32 + 0.5) as i32;
        }
        if percent > 100 {
            percent = 100;
        }
        percent
    }
}

pub struct ProgressSpinner {
    meter: ProgressMeter,
}

impl fmt::Display for ProgressSpinner {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if ! self.meter.label.is_empty() {
            write!(f, "{} ", &self.meter.label)?;
        }

        const SPIN: &str = r"|/-\";

        write!(f, "{} ", SPIN.chars().nth(self.meter.value as usize).unwrap())?;

        if ! self.meter.rlabel.is_empty() {
            write!(f, "{} ", &self.meter.rlabel)?;
        }

        Ok(())
    }
}

impl Progress for ProgressSpinner {
    fn get_value(&self) -> i32 {
        return self.meter.value;
    }

    fn get_max_value(&self) -> i32 {
        return self.meter.max_value;
    }

    fn set_label(&mut self, label: &str) {
        self.meter.set_label(label);
    }

    fn set_rlabel(&mut self, rlabel: &str) {
        self.meter.set_rlabel(rlabel);
    }

    fn set_value(&mut self, _value: i32) {
        self.meter.value = 0;
    }

    fn set_max_value(&mut self, _value: i32) {
        // not used for spinners
        self.meter.max_value = 0;
    }

    fn show(&self) {
        print!("{}", &self);
        stdout().flush().unwrap();
    }

    fn hide(&self) {
        if self.meter.have_vt100 {
            print!("\r\x1b[K");
        } else {
            let length = 2 + self.meter.label.len() + 1 + self.meter.rlabel.len() + 1;
            print!("\r{: <1$}\r", "", length);
        }
        stdout().flush().unwrap();
    }

    fn update(&mut self, value: i32) {
        if self.meter.need_update() {
            self.update_value(value);
            self.update_display();
        }
    }

    fn update_value(&mut self, _value: i32) {
        self.meter.value += 1;
        if self.meter.value >= 4 {
            self.meter.value = 0;
        }
    }

    fn update_display(&self) {
        self.meter.back_rlabel();

        const SPIN: &str = r"|/-\";

        print!("\x08\x08{} ", SPIN.chars().nth(self.meter.value as usize).unwrap());

        if ! self.meter.rlabel.is_empty() {
            print!("{} ", &self.meter.rlabel);
        }
        stdout().flush().unwrap();
    }

    fn finish(&self) {
        self.meter.erase_rlabel();

        print!("\x08\x08  \x08\x08");

        if ! self.meter.rlabel.is_empty() {
            println!("{}", &self.meter.rlabel);
        } else {
            println!();
        }
    }
}

impl ProgressSpinner {
    pub fn new() -> ProgressSpinner {
        ProgressSpinner {
            meter: ProgressMeter::new(),
        }
    }

    pub fn new_spinner(label: &str, rlabel: &str) -> ProgressSpinner {
        ProgressSpinner {
            meter: ProgressMeter::new_meter(label, rlabel, 0),
        }
    }
}

// EOB
