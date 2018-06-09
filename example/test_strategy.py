# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.strategy_center.strategy import StrategyBase

from AmazingQuant.environment import Environment

class MaStrategy(StrategyBase):

    def initialize(self):
        self.capital = 200000
        self.benchmark = "000001.SH"
        self.start = "20170101"
        self.end = "20170201"
        self.period = "daily"
        print(self.start)

    def handle_bar(self):
        print(self.benchmark)


if __name__ == "__main__":

    Environment.account["qwe"] = 1
    MaStrategy().run()
    print(Environment.account)
    Environment.refresh()
    print(Environment.account)