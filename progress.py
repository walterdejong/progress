#
#   progress.py WJ118
#
#   * written by Walter de Jong <walter@heiho.net>
#   * This is free and unencumbered software released into the public domain.
#     Please refer to http://unlicense.org/
#

'''progress meters'''

import time

_FPS_RATE = 4


class Meter:
    '''base class for a progress meter'''

    def __init__(self, label: str='', rlabel: str='', start_value: int=0,
                 clear: bool=True, rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        self.label = label
        self.rlabel = rlabel
        self.clear = clear
        self.value = start_value
        self.rate = rate
        self.visible = False
        self.timestamp = 0.0
        self.line = ''

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

        self.back()

        if self.label:
            print('\r' + ' ' * (len(self.label) + 1), end='', flush=False)

        self.erase()

        print('\r', end='', flush=True)

    def _render(self) -> None:
        '''make output and display it'''

        self.back()

        line = self.render() + ' '
        if self.rlabel:
            line += self.rlabel + ' '

        if line == self.line:
            return

        self.line = line
        self.display()

    def display(self) -> None:
        '''display the meter'''

        print(self.line, end='', flush=True)

    def back(self) -> None:
        '''move cursor back'''

        print('\b' * len(self.line), end='', flush=False)

    def erase(self) -> None:
        '''erase the meter'''

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

        return 'not yet implemented'



class Bar(Meter):
    '''represents a progress bar'''

    def __init__(self, max_value: int, label: str='', rlabel: str='', start_value: int=0,
                 width: int=20, face: str='| =|', rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, start_value=start_value, clear=False, rate=rate)

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

        return (self.face[0] + self.face[2] * units + self.face[1] * (self.width - units) +
                self.face[-1] + ' {}'.format(self.value))



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

    def update(self) -> None:   # type: ignore
        '''overridden update() func without arguments'''

        super().update(self.value)



class Percent(Meter):
    '''represents a percentage meter'''

    def __init__(self, max_value: int, label: str='', rlabel: str='',
                 start_value: int=0, rate: float=_FPS_RATE) -> None:
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, start_value=start_value, clear=False, rate=rate)

        self.max_value = max_value
        self.value = start_value

    def render(self) -> str:
        '''Returns percent counter to display'''

        one_percent = 100 / self.max_value
        value = self.value
        if value > self.max_value:
            value = self.max_value

        percent = int(value * one_percent)
        return '{}%'.format(percent)

    def finish(self) -> None:
        '''end the progress meter'''

        # always display as 100%
        self.value = self.max_value
        self._render()

        self.reset()
        print('')



def _test_percent():
    '''test Percent'''

    meter = Percent(label='processing ...', max_value=1024)
    meter.show()
 
    value = 0
    for i in range(100):
        time.sleep(0.1)
        value += 10
        meter.update(value)

    meter.finish()


def _test_bar():
    '''test Bar'''

    meter = Bar(label='downloading', max_value=1000000, rlabel='bytes')
    meter.show()
 
    value = 0
    for i in range(100):
        time.sleep(0.1)
        value += 11024
        meter.update(value)

    meter.finish()


def _test_spinner():
    '''test Spinner'''

    spinner = Spinner('busy ...', rlabel='please wait')
    spinner.show()
    
    for i in range(100):
        time.sleep(0.1)
        spinner.update()

    spinner.finish()



if __name__ == '__main__':
    _test_bar()
    _test_spinner()
    _test_percent()


# EOB
