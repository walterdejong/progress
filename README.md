progress
========

I keep running into ugly and badly programmed progress meters, so ...
this is a module for progress bars / counters. ~~It's Python3, but~~ you
can easily adopt the main idea of this code for other programming
languages.

The trick with ASCII progress meters is that you should not update
the screen more than four times per second, or there will be flicker and
a very restless terminal.

Now, rather than truly minimizing the character updates, we can be
a little lazy and simply redraw the entire progress meter every so often.


Languages
---------

Codes plus examples are included for:

- Python3
- good old C
- Go (golang)
- Rust

Note that the codes are similar, but they are not straight ports.


Usage
-----

1. Progress bar

Starts at zero, fills up to maximum value.
You need to call `update()` with the current value sometimes,
but you can call it as often as you like.

```python
    import progress

    bar = progress.Bar(max_value=7699908)
    bar.show()

    while doing_work:
        ...
        bar.update(current_value)

    bar.finish()
```

2. Spinner

Use when you don't know the maximum value, but want to indicate
that the program is busy.
Call `update()`, and call it as often as you like.

```python
    import progress

    spinner = progress.Spinner()
    spinner.show()

    while doing_work:
        ...
        spinner.update()

    spinner.finish()
```

3. Percentage counter

Guess what this thing does.

```python
    import progress

    percent = progress.Percent(max_value=15415265)
    percent.show()

    while doing_work:
        ...
        percent.update(current_value)

    percent.finish()
```

Each of these types may also take a parameter `label` and/or `rlabel`,
for placing text left and right of the progress meter.
You might also display the value in a slightly different way by passing
a custom `formatter` function. If that doesn't suffice, you can subclass
the type and override the `render()` method to fully customize the
progress meter. It's also possible to implement a completely new type of
meter by subclassing `progress.Meter`.


Multi-threaded (Python)
-----------------------

Up till now we've been single-threaded and we had to explicitly call
`update()`. We can also let the progress be monitored from a thread.
A threaded meter can `start()` and `stop()`. After `stop()` returns,
it is guaranteed that the thread has gone away. So using a threaded
progress meter is easy, just be sure to update the `meter.value`
while doing work.

1. Threaded progress bar

```python
    value = 0
    max_value = 1265276
    meter = progress.ThreadBar(max_value=max_value)
    meter.start()

    # main thread is really busy here
    while value < max_value:
        do_work()
        value += n
        meter.value = value

    meter.stop()
```

2. Threaded spinner

```python
    spinner = progress.ThreadSpinner()
    spinner.start()

    while doing_work:
        do_work()

    spinner.stop()
```

1. Threaded percentage counter

```python
    value = 0
    max_value = 1265276
    meter = progress.Percent(max_value=max_value)
    meter.start()

    # main thread is really busy here
    while value < max_value:
        do_work()
        value += n
        meter.value = value

    meter.stop()
```

Just as with the single-threaded versions, the looks can be customized with
labels and number formatters, or you might subclass to customize the
threaded progress meter.

------
_This is free and unencumbered software released into the public domain._
