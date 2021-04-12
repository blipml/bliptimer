#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt, timedelta
from time import time, sleep
import sys
import asyncio

SLEEP_TIME=1

class TimeParseException(Exception):
    pass


class Timer(object):

    def __init__(
        self, target=0, sleep_time=SLEEP_TIME):
        self.target = Timer.parse_time(sys.argv[1])
        self.elapsed = 0
        print(self.target)
        self.sleep_time = sleep_time

    @staticmethod
    def parse_time(string):
        mul = [60*60, 60, 1][::-1]
        components = string.split(':')[::-1]

        if len(components) > len(mul):
            raise TimeParseException()
        elif len(components) != len(mul):
            mul = mul[:len(components)-len(mul)]

        _sum = 0
        for m, c in zip(mul, components):
            _sum += m*int(c)
        return _sum

    def start_timer(self):
        last = now = time()

        while(self.elapsed < self.target):
            self.elapsed = now-last
            sleep(self.sleep_time)
            now = time()
            self.tick_callback()
        self.end_callback()

    def tick_callback(self):
        pass
    
    def end_callback(self):
        pass


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
        # self.task.cancel()
        pass


class Pomodowo(Timer):

    def __init__(self, *args, **kwargs):
        super(Pomodowo, self).__init__(*args, **kwargs)

    def tick_callback(self):
        """
            we can access tick level information here
        """
        outfile = './discordtimer'
        header = 'pomod🍅w🍅'
        output = "{}\n\r◇{}◇".format(header, str(
                                    timedelta(seconds=round(
                                        self.target-self.elapsed))))

        with open(outfile, 'w') as f:
            f.write(output)
        print(output)


class WaterTimer(Timer):

    def __init__(self,*args, **kwargs):
        super(WaterTimer, self).__init__(*args, **kwargs)
    
    def end_callback(self):
        # control OBS scene?

        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Pass me a target for the timer format [HH]:[mm]:ss")
        exit()

    t = Pomodowo(sys.argv[1])
    t.start_timer()
