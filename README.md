progress
========

A Python module for progress bars / counters.

I keep running into ugly and badly programmed progress meters, so ...

The trick with ASCII progress meters is that you should not update
the screen more than four times per second, or there will be flicker and
a very restless terminal.

Now, rather than truly minimizing the character updates, we can be
a little lazy and simply redraw the entire progress meter every so often.


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

These classes are all derived from the base `progress.Meter`.
You might add a new type of meter by deriving from `progress.Meter`.


--
This is free and unencumbered software released into the public domain.

