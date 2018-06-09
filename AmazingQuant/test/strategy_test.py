# -*- coding: utf-8 -*-

__author__ = "gao"

from abc import ABCMeta, abstractmethod


class strategy(metaclass=ABCMeta):
    def __init__(self):
        self._start = '5'

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    def run(self):
        self.initialize()
        self.handle_bar()

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def handle_bar(self):
        pass


class B(strategy):

    def initialize(self):
        self.s1 = "000001.XSHE"
        self.SHORTPERIOD = 20
        self.LONGPERIOD = 120
        # self.start = '5'
        print(self.start)

    def handle_bar(self):
        print(self.LONGPERIOD)


if __name__ == "__main__":
    C = B()
    C.run()
