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
        self._end = "2018-01-02"
        self._benchmark = "000300.SH"
        self._period = Period.DAILY.value  # 后续支持1min 3min 5min 等多周期
        self._universe = [self._benchmark]
        self._rights_adjustment = RightsAdjustment.NONE.value
        self._timetag = 0
        # 取数据
        self._get_data = GetData()
        # 缓存日线数据
        self._daily_data_cache = False
        self._daily_data = None
        # 换存分钟线数据
        self._one_min_data_cache = False
        self._one_min_data = None

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
    def benchmark(self):
        return self._benchmark

    @benchmark.setter
    def benchmark(self, value):
        self._benchmark = value

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

    @property
    def daily_data_cache(self):
        return self._daily_data_cache

    @daily_data_cache.setter
    def daily_data_cache(self, value):
        self._daily_data_cache = value

    @property
    def daily_data(self):
        return self._daily_data

    @daily_data.setter
    def daily_data(self, value):
        self._daily_data = value

    @property
    def one_min_data_cache(self):
        return self._one_min_data_cache

    @one_min_data_cache.setter
    def one_min_data_cache(self, value):
        self._one_min_data_cache = value

    @property
    def one_min_data(self):
        return self._one_min_data

    @one_min_data.setter
    def one_min_data(self, value):
        self._one_min_data = value

    def run(self, run_mode=RunMode.BACKTESTING.value):
        self.initialize()
        print(self.benchmark, self.start, self.end, self.period, self.rights_adjustment)
        if run_mode == RunMode.TRADE.value:
            self.end = self._get_data.get_end_timetag(benchmark=self.benchmark, period=Period.DAILY.value)

        daily_data = self._get_data.get_all_market_data(stock_code=self.universe,
                                                        field=["open", "high", "low", "close", "volumn", "amount"],
                                                        end=self.end, period=self.period)

        benchmark_index = [data_transfer.date_to_millisecond(str(int(i)), '%Y%m%d') for i in
                           daily_data["open"].ix[self.benchmark].index
                           if i >= data_transfer.date_str_to_int(self.start)]
        if self.daily_data_cache:
            self.daily_data = daily_data
            # print(self.daily_data_cache)
        if self.one_min_data_cache:
            """
            补充完分钟数据，再缓存ｍｉｎ数据
            """
            self.one_min_data = one_min_data

        bar_index = 0
        while True:
            try:
                self.timetag = benchmark_index[bar_index]
            except IndexError:
                if run_mode == RunMode.BACKTESTING.value:
                    break
                elif run_mode == RunMode.TRADE.value:
                    '''读取最新tick, 更新最新的分钟或者日线
                    if 读取最新tick, 更新最新的分钟或者日线 == done:
                        daily_data.append(new_day_data)
                        bar_index += 1
                        benchmark_index.append(new_day_timetag)
                    '''
                    pass

            else:

                date = int(data_transfer.millisecond_to_date(millisecond=self.timetag, format="%Y%m%d"))
                # ee.start() event 做执行下面两个事件

                # （１）用当前bar的收盘价更新资金  持仓
                # print(daily_data["close"].ix["000300.SH"][date])
                # print(self.capital)
                # print(Environment.account)
                # print(Environment.position)
                # (2) 跑每一根bar
                self.handle_bar()
                bar_index += 1
                # ee.stop()

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def handle_bar(self):
        pass
