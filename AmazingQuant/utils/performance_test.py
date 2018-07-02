# -*- coding: utf-8 -*-

__author__ = "gao"

from time import *


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = clock()
        return self

    def __exit__(self, *args):
        self.end = clock()
        self.secs = self.end - self.start
        self.millisecond = self.secs * 1000  # millisecond
        if self.verbose:
            print('elapsed time: %f ms' % self.millisecond)
