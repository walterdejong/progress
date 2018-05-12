#
#   progress.py WJ118
#
#   * written by Walter de Jong <walter@heiho.net>
#   * This is free and unencumbered software released into the public domain.
#     Please refer to http://unlicense.org/
#

'''progress meters'''

import time

_FPS_RATE = 0.25


class Meter:
    '''base class for a progress meter'''

    def __init__(self, label='', rlabel='', clear=True, rate=_FPS_RATE):
        '''initialize instance'''

        self.label = label
        self.rlabel = rlabel
        self.clear = clear
        self.value = 0
        self.rate = rate
        self.visible = False
        self.timestamp = 0
        self.line = ''

    def show(self):
        '''show the progress meter'''

        if self.visible:
            return

        if self.label:
            print(self.label + ' ', end='', flush=False)

        self._render()
        self.visible = True
        self.timestamp = time.monotonic()

    def hide(self):
        '''hide the progress meter'''

        self.visible = False

        self.back()

        if self.label:
            print('\r' + ' ' * (len(self.label) + 1), end='', flush=False)

        self.erase()

        print('\r', end='', flush=True)

    def _render(self):
        '''make output and display it'''

        self.back()

        line = self.render() + ' '
        if self.rlabel:
            line += self.rlabel + ' '

        if line == self.line:
            return

        self.line = line
        self.display()

    def display(self):
        '''display the meter'''

        print(self.line, end='', flush=True)

    def back(self):
        '''move cursor back'''

        print('\b' * len(self.line), end='', flush=False)

    def erase(self):
        '''erase the meter'''

        print(' ' * len(self.line), end='', flush=True)

    def update(self):
        '''update and show progress meter'''

        if not self.visible:
            self.show()
            return

        curr_time = time.monotonic()
        diff_time = curr_time - self.timestamp
        if diff_time < self.rate:
            return

        self.timestamp = curr_time

        self._render()

    def finish(self):
        '''end the progress meter'''

        if self.clear:
            self.hide()
        else:
            # display final value
            self._render()
            print('')

        self.reset()
        self.visible = False

    def reset(self):
        '''reset the progress meter to start'''

        self.value = 0
        self.line = ''

    def render(self):
        '''Returns the rendered line'''

        # you should override this method

        return 'not yet implemented'



class Bar(Meter):
    '''represents a progress bar'''

    def __init__(self, max_value, label='', rlabel='', start_value=0,
                 width=20, face='| =|', rate=_FPS_RATE):
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, clear=False, rate=rate)

        self.max_value = max_value
        self.value = start_value
        self.width = width
        self.face = face

    def render(self):
        '''Returns the meter to display'''

        one_unit = self.width / self.max_value
        value = self.value
        if value > self.max_value:
            value = self.max_value
        units = int(value * one_unit + 0.5)

        return (self.face[0] + self.face[2] * units + self.face[1] * (self.width - units) +
                self.face[-1] + ' {}'.format(self.value))

    def update(self, value):
        '''update and show progress meter'''

        self.value = value
        super().update()



class Spinner(Meter):
    '''represents a spinner'''

    def __init__(self, label='', rlabel='', rate=_FPS_RATE):
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, clear=True, rate=rate)

        self.value = 0
        self.face = '|/-\\'

    def render(self):
        '''make output and display it'''

        # update and render
        self.value += 1
        if self.value >= len(self.face):
            self.value = 0

        return self.face[self.value]



class Percent(Meter):
    '''represents a percentage meter'''

    def __init__(self, max_value, label='', rlabel='', start_value=0, rate=_FPS_RATE):
        '''initialize instance'''

        super().__init__(label=label, rlabel=rlabel, clear=False, rate=rate)

        self.max_value = max_value
        self.value = start_value

    def render(self):
        '''Returns meter to display'''

        one_percent = 100 / self.max_value
        value = self.value
        if value > self.max_value:
            value = self.max_value

        percent = int(value * one_percent)
        return '{}%'.format(percent)

    def update(self, value):
        '''update and show progress meter'''

        self.value = value

        super().update()

    def finish(self):
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
