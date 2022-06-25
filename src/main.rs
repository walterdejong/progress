/*
    progress WJ112
    main.rs : progress demonstrator program

    * written by Walter de Jong <walter@heiho.net>
    * This is free and unencumbered software released into the public domain.
      Please refer to http://unlicense.org/


    this is a rather crappy program but it is only intended to show
    how to use the progress indicators: ProgressBar, ProgressPercent, ProgressSpinner

    - step 1 : make a progress indicator instance
               either with ::new() or with ::new_bar() / ::new_percent() / ::new_spinner()
    - step 2 : .show() the indicator
    - step 3 : repeatedly call .update() while doing work, usually in a loop
               do this until you finish doing work
    - step 4 : call .finish() to render the final state of the indicator
*/

use progress::{Progress, ProgressSpinner, ProgressPercent, ProgressBar};

use std::{thread, time};


fn main() {
    let mut bar = ProgressBar::new_bar("downloading", "linux.tar.gz", 2560, 20);
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
