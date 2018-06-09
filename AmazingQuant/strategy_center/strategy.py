# -*- coding: utf-8 -*-

__author__ = "gao"

from abc import ABCMeta, abstractmethod

from AmazingQuant.constant import RunMode, Period, RightsAdjustment
from AmazingQuant.environment import Environment


class StrategyBase(metaclass=ABCMeta):
    def __init__(self):
        self._capital = 1000000
        self._start = "20170101"
        self._end = "20180101"
        self._benckmark = "000300.SH"
        self._period = Period.DAILY  # 后续支持1min 3min 5min 等多周期
        self._universe = [self._benckmark]
        self._rights_adjustment = RightsAdjustment.NONE.value

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, value):
        self._capital = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def benckmark(self):
        return self._benckmark

    @benckmark.setter
    def benckmark(self, value):
        self._benckmark = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value

    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, value):
        self._universe.append(value)

    @property
    def rights_adjustment(self):
        return self._rights_adjustment

    @rights_adjustment.setter
    def rights_adjustment(self, value):
        self._rights_adjustment = value

    def run(self, run_mode=RunMode.BACKTESTING.value):
        if run_mode == RunMode.BACKTESTING.value:
            self.initialize()
            print(self.universe, self.start, self.end, self.period, self.rights_adjustment)

            print(self.capital)
            print(Environment.account)
            print(Environment.position)
            self.handle_bar()
        elif run_mode == RunMode.TRADE.value:
            pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def handle_bar(self):
        pass
