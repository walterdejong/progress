//

use progress::{Progress, ProgressSpinner, ProgressPercent, ProgressBar};

use std::{thread, time};


fn main() {
    let mut bar = ProgressBar::new_bar("downloading", "linux.tar.gz", 2560, 22);
    bar.show();
    for _i in 0..100 {
        bar.update(bar.get_value() + 15);
        thread::sleep(time::Duration::from_millis(50));
    }
    bar.set_value(bar.get_max_value());
    bar.finish();

    let mut percent = ProgressPercent::new();
    percent.set_label("processing");
    percent.set_rlabel("done");
    percent.set_max_value(2560);
    percent.show();
    for _i in 0..100 {
        percent.update(percent.get_value() + 15);
        thread::sleep(time::Duration::from_millis(50));
    }
    percent.set_value(percent.get_max_value());
    percent.hide();
    percent.finish();

    println!();

    let mut spinner = ProgressSpinner::new();
    spinner.set_label("working");
    spinner.set_rlabel("(please wait)");
    spinner.show();
    for _i in 0..100 {
        spinner.update(1);
        thread::sleep(time::Duration::from_millis(50));
    }
    //spinner.hide();
    spinner.finish();
}

// EOB
