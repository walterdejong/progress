#
#   progress.py WJ118
#
#   * written by Walter de Jong <walter@heiho.net>
#   * This is free and unencumbered software released into the public domain.
#     Please refer to http://unlicense.org/
#

'''progress meters'''

import os
import time
import threading

from typing import Callable

_FPS_RATE = 4


class Meter:
    '''base class for a progress meter'''

    def __init__(self, label: str='', rlabel: str='', start_value: int=0,
                 formatter: Callable[[float], str]=None,
                 clear: bool=True, rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        self.label = label
        self.rlabel = rlabel
        self.value = start_value
        self.clear = clear
        self.formatter = formatter
        self.rate = rate
        self.visible = False
        self.timestamp = 0.0
        self.line = ''
        try:
            self.vt100 = (os.environ['TERM'] != 'dumb')
        except KeyError:
            self.vt100 = False

    def show(self) -> None:
        '''show the progress meter'''

        if self.visible:
            return

        if self.label:
            print(self.label + ' ', end='', flush=False)

        self._render()
        self.visible = True
        self.timestamp = time.monotonic()

    def hide(self) -> None:
        '''hide the progress meter'''

        self.visible = False

        if self.vt100:
            print('\r\x1b[K', end='', flush=True)
        else:
            if self.label:
                print('\r' + ' ' * (len(self.label) + 1), end='', flush=False)
            else:
                self.back()
            self.erase()
            print('\r', end='', flush=True)

    def _render(self) -> None:
        '''make output and display it'''

        line = self.render() + ' '
        if self.rlabel:
            line += self.rlabel + ' '

        if line == self.line:
            return

        self.back()
        self.line = line
        self.display()

    def display(self) -> None:
        '''display the meter'''

        print(self.line, end='', flush=True)

    def back(self) -> None:
        '''move cursor back'''

        if self.line:
            if self.vt100:
                print('\x1b[{}D'.format(len(self.line)), end='', flush=False)
            else:
                print('\b' * len(self.line), end='', flush=False)

    def erase(self) -> None:
        '''erase the meter'''

        if self.vt100:
            print('\x1b[K', end='', flush=True)
        else:
            print(' ' * len(self.line), end='', flush=True)

    def update(self, value: int) -> None:
        '''update and show progress meter'''

        self.value = value

        if not self.visible:
            self.show()
            return

        curr_time = time.monotonic()
        diff_time = curr_time - self.timestamp
        if diff_time < 1.0 / self.rate:
            return

        self.timestamp = curr_time
        self._render()

    def finish(self) -> None:
        '''end the progress meter'''

        if self.clear:
            self.hide()
        else:
            # display final value
            self._render()
            print('')

        self.reset()
        self.visible = False

    def reset(self) -> None:
        '''reset the progress meter to start'''

        self.value = 0
        self.line = ''

    def render(self) -> str:
        '''Returns the rendered line'''

        # you should override this method

        if self.formatter is not None:
            return self.formatter(float(self.value))

        return '{}'.format(self.value)



class Bar(Meter):
    '''represents a progress bar'''

    def __init__(self, max_value: int, label: str='', rlabel: str='', start_value: int=0,
                 width: int=20, face: str='| =|', formatter: Callable[[float], str]=None,
                 rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, start_value=start_value,
                         clear=False, formatter=formatter, rate=rate)

        self.max_value = max_value
        self.width = width
        self.face = face

    def render(self) -> str:
        '''Returns the bar to display'''

        one_unit = self.width / self.max_value
        value = self.value
        if value > self.max_value:
            value = self.max_value
        units = int(value * one_unit + 0.5)

        if self.formatter is not None:
            v = self.formatter(float(self.value))
        else:
            v = '{}'.format(self.value)

        return (self.face[0] + self.face[2] * units + self.face[1] * (self.width - units) +
                self.face[-1] + ' ' + v)



class Spinner(Meter):
    '''represents a spinner'''

    def __init__(self, label: str='', rlabel: str='', rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, clear=True, rate=rate)

        self.face = '|/-\\'

    def render(self) -> str:
        '''Returns the spinner animation frame to display'''

        # update and render
        self.value += 1
        if self.value >= len(self.face):
            self.value = 0

        return self.face[self.value]

    def update(self, value: int=0) -> None:
        '''overridden update() func without arguments'''

        super().update(self.value)



class Percent(Meter):
    '''represents a percentage meter'''

    def __init__(self, max_value: int, label: str='', rlabel: str='',
                 start_value: int=0, formatter: Callable[[float], str]=None,
                 rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, start_value=start_value,
                         clear=False, formatter=formatter, rate=rate)

        self.max_value = max_value
        self.value = start_value

    def render(self) -> str:
        '''Returns percent counter to display'''

        one_percent = 100 / self.max_value
        value = self.value
        if value > self.max_value:
            value = self.max_value
        percent = value * one_percent

        if percent >= 100:
            return '100%'
        else:
            if self.formatter is None:
                v = '{}'.format(int(percent))
            else:
                v = self.formatter(percent)

            return v + '%'

    def finish(self) -> None:
        '''end the progress meter'''

        # always display as 100%
        self.value = self.max_value
        self._render()

        self.reset()
        print('')



class ThreadMeter(threading.Thread):
    '''secondary base class to make a threaded Meter'''

    # Note: this is a component class, that should be combined
    # with a progress.Meter

    def __init__(self):
        '''initialize instance'''

        super().__init__()

        self.running = False

    def run(self) -> None:
        '''run the thread'''

        self.running = True

        self.show()

        rate = 1 / self.rate
        while self.running:
            time.sleep(rate)
            self.update(self.value)

        self.finish()

    def stop(self) -> None:
        '''stop running'''

        self.running = False
        self.join()



class ThreadSpinner(ThreadMeter, Spinner):
    '''a threaded spinner'''

    def __init__(self, label: str='', rlabel: str='', rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        Spinner.__init__(self, label=label, rlabel=rlabel, rate=rate)
        ThreadMeter.__init__(self)



class ThreadBar(ThreadMeter, Bar):
    '''a threaded progress bar'''

    def __init__(self, max_value: int, label: str='', rlabel: str='', start_value: int=0,
                 width: int=20, face: str='| =|', formatter: Callable[[float], str]=None,
                 rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        Bar.__init__(self, max_value=max_value, label=label, rlabel=rlabel, start_value=start_value,
                     width=width, face=face, formatter=formatter, rate=rate)
        ThreadMeter.__init__(self)



class ThreadPercent(ThreadMeter, Percent):
    '''a threaded percentage meter'''

    def __init__(self, max_value: int, label: str='', rlabel: str='',
                 start_value: int=0, formatter: Callable[[float], str]=None,
                 rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        Percent.__init__(self, max_value=max_value, label=label, rlabel=rlabel, start_value=start_value,
                         formatter=formatter, rate=rate)
        ThreadMeter.__init__(self)



def _test_percent() -> None:
    '''test Percent'''

    value = 0
    max_value = 1024
    meter = Percent(label='processing ...', max_value=max_value, start_value=value)
    meter.show()

    while value < max_value:
        value += 15
        time.sleep(0.1)
        meter.update(value)

    meter.finish()


def _test_percentf() -> None:
    '''test Percentf'''

    def format_float(value: float) -> str:
        '''local function; format with a decimal point'''

        return '{:.1f}'.format(value)

    value = 0
    max_value = 1024
    meter = Percent(label='processing ...', max_value=max_value, start_value=value,
                    formatter=format_float)
    meter.show()

    while value < max_value:
        value += 15
        time.sleep(0.1)
        meter.update(value)

    meter.finish()


def _test_bar() -> None:
    '''test Bar'''

    def format_number(value: float) -> str:
        '''local function: formats the value'''

        # format with comma for thousands separator

        return '{:,}'.format(int(value))

    value = 0
    max_value = 50 * 11024
    meter = Bar(label='downloading', max_value=max_value, start_value=value,
                rlabel='bytes', formatter=format_number)
    meter.show()

    while value < max_value:
        time.sleep(0.1)
        value += 11024
        meter.update(value)

    meter.finish()


def _test_spinner() -> None:
    '''test Spinner'''

    spinner = Spinner('busy ...', rlabel='please wait')
    spinner.show()

    for _i in range(70):
        time.sleep(0.1)
        spinner.update()

    spinner.finish()


def _test_threadspinner() -> None:
    '''test ThreadSpinner'''

    spinner = ThreadSpinner('(thread) busy ...', rlabel='please wait')
    spinner.start()

    # main thread is really busy here
    time.sleep(7)

    spinner.stop()
    # spinner is guaranteed to have stopped now
    # ok to continue main thread


def _test_threadbar() -> None:
    '''test ThreadBar'''

    def format_number(value: float) -> str:
        '''local function: formats the value'''

        # format with comma for thousands separator

        return '{:,}'.format(int(value))

    value = 0
    max_value = 50 * 11024
    meter = ThreadBar(label='(thread) downloading', max_value=max_value, start_value=value,
                      rlabel='bytes', formatter=format_number)
    meter.start()

    # main thread is really busy here
    while value < max_value:
        value += 11024
        meter.value = value
        time.sleep(0.1)

    meter.stop()
    # meter is guaranteed to have stopped now
    # ok to continue main thread


def _test_threadpercent() -> None:
    '''test ThreadPercent'''

    def format_float(value: float) -> str:
        '''local function; format with a decimal point'''

        return '{:.1f}'.format(value)

    value = 0
    max_value = 1024
    meter = ThreadPercent(label='(thread) processing ...', max_value=max_value, start_value=value,
                          formatter=format_float)
    meter.start()

    # main thread is really busy here
    while value < max_value:
        value += 15
        meter.value = value
        time.sleep(0.1)

    meter.stop()
    # meter is guaranteed to have stopped now
    # ok to continue main thread



if __name__ == '__main__':
    _test_bar()
    _test_spinner()
    _test_percent()
    _test_percentf()

    _test_threadbar()
    _test_threadspinner()
    _test_threadpercent()


# EOB
