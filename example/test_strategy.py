# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.strategy_center.strategy import StrategyBase
from AmazingQuant.environment import Environment
import AmazingQuant.utils.data_transfer as data_transfer


class MaStrategy(StrategyBase):

    def initialize(self):
        self.capital = 200000
        self.benchmark = "000001.SH"
        self.start = "2017-01-01"
        self.end = "2017-02-21"
        self.period = "daily"
        self.universe = ["000002.SZ", "000001.SH"]
        print(self.start)

    def handle_bar(self):
        print(self.benchmark)
        #print(self.timetag)
        #print(data_transfer.millisecond_to_date(millisecond=self.timetag, format="%Y-%m-%d"))

if __name__ == "__main__":
    Environment.account["qwe"] = 1
    MaStrategy().run()
    # print(Environment.account)
    Environment.refresh()
    # print(Environment.account)
