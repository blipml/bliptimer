#! python3

from datetime import datetime as dt, timedelta
from time import time, sleep
import sys
import asyncio

SLEEP_TIME=1

class TimeParseException(Exception):
    pass


class Timer(object):

    def __init__(self, target=0, callback=None, sleep_time=SLEEP_TIME):
        assert(callback is not None)

        self.target = target
        self.mul = [60*60, 60, 1][::-1]
        self.callback = callback
        self.sleep_time = sleep_time

    def parse_time(self, string):
        components = string.split(':')[::-1]

        if len(components) > len(self.mul):
            raise TimeParseException()
        elif len(components) != len(self.mul):
            self.mul = self.mul[:len(components)-len(self.mul)]

        _sum = 0
        for m, c in zip(self.mul, components):
            _sum += m*int(c)
        return _sum


    def start_timer(self):
        target = self.parse_time(sys.argv[1]) + 1
        last = now = time()

        while((now-last) < target):
            sleep(self.sleep_time)
            now = time()
            self.callback(target, now-last)


class AsyncTimer(Timer):
    # implement coroutines for callbacks?
    def __init__(self, *args, **kwargs):
        super(AsyncTimer, self).__init__(*args, **kwargs)
        self.task = None # ???


class PreemptAsyncTimer(AsyncTimer):
    # do we want to be able to somehow pre-empt timers?
    def __init__(self, *args, **kwargs):
        super(PreemptAsyncTimer, self).__init__(*args, **kwargs)
    
    def cancel(self):
        # maybe we don't want this here :)
        self.task.cancel()


def printcback(target, elapsed):
    outfile = '/home/ocean/workspace/blip/discordtimer'
    header = 'pomod🍅w🍅'
    output = "{}\n\r◇{}◇".format(
        header, str(timedelta(seconds=round(target-elapsed))))

    with open(outfile, 'w') as f:
        f.write(output)
    print(output)


# how do we even define a widget, class, method???
def widget(target,elapsed):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Pass me a target for the timer format [HH]:[mm]:ss")
        exit()

    t = Timer(sys.argv[1], printcback)
    t.start_timer()
