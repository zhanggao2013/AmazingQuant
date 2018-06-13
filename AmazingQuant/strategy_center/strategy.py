# -*- coding: utf-8 -*-

__author__ = "gao"

from abc import ABCMeta, abstractmethod

import AmazingQuant.utils.data_transfer as data_transfer
from AmazingQuant.constant import RunMode, Period, RightsAdjustment
from AmazingQuant.environment import Environment
from AmazingQuant.data_center.get_data import GetData


class StrategyBase(metaclass=ABCMeta):
    def __init__(self):
        self._capital = 1000000
        self._start = "2017-01-01"
        self._end = "2018-01-01"
        self._benckmark = "000300.SH"
        self._period = Period.DAILY  # 后续支持1min 3min 5min 等多周期
        self._universe = [self._benckmark]
        self._rights_adjustment = RightsAdjustment.NONE.value
        self._timetag = 0
        # 取数据
        self._get_data = GetData()

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
        self._universe.extend(value)

    @property
    def rights_adjustment(self):
        return self._rights_adjustment

    @rights_adjustment.setter
    def rights_adjustment(self, value):
        self._rights_adjustment = value

    @property
    def timetag(self):
        return self._timetag

    @timetag.setter
    def timetag(self, value):
        self._timetag = value

    def run(self, run_mode=RunMode.BACKTESTING.value):
        if run_mode == RunMode.BACKTESTING.value:
            self.initialize()
            print(self.universe, self.start, self.end, self.period, self.rights_adjustment)

            market_data = self._get_data.get_market_data(stock_code=self.universe,
                                                         field=["open", "high", "low", "close", "volumn", "amount"],
                                                         start="0", end=self.end, period=self.period,
                                                         skip_paused=True, rights_adjustment=self.rights_adjustment,
                                                         count=-1)
            benchmark_index = [data_transfer.date_to_millisecond(str(int(i)), '%Y%m%d') for i in
                               market_data["open"].ix[self.benckmark].index
                               if i >= data_transfer.date_str_to_int(self.start)]
            for bar_timetag in range(len(benchmark_index)):
                self.timetag = benchmark_index[bar_timetag]
                # print(self.timetag)
                date = int(data_transfer.millisecond_to_date(millisecond=self.timetag, format="%Y%m%d"))

                print(market_data["open"].ix["000300.SH"][date])
                self.handle_bar()
                print(market_data["close"].ix["000300.SH"][date])

                # print(self.capital)
                # print(Environment.account)
                # print(Environment.position)
        elif run_mode == RunMode.TRADE.value:
            pass

    @abstractmethod
    def initialize(self):
        pass


    @abstractmethod
    def handle_bar(self, timetag):
        pass


"""
        if run_mode == RunMode.TRADE.value:
            self.end = float("inf")
        i = 0
        while True:
            try:
                bar = benchmark_index[i]
            except no exist:
                if run_mode == RunMode.BACKTESTING.value:
                    break
                elif run_mode == RunMode.TRADE.value:
                    读取最新tick, 更新最新的分钟或者日线
                    if 读取最新tick, 更新最新的分钟或者日线 == done:
                        data.append(new_day_data)
                        i += 1
                        index.append(new_day_timetag)
            else:
                ee.start()
                i += 1
                ee.stop()

"""
