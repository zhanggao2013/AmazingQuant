# -*- coding: utf-8 -*-

__author__ = "gao"

from strategy_center.strategy import StrategyBase
class MaStrategy(StrategyBase):

    def initialize(self):
        self.benchmark = "000001.SH"
        self.start = "20170101"
        self.end = "20170201"
        self.period = "day"
        print(self.start)

    def handle_bar(self):
        print(self.benchmark)


if __name__ == "__main__":
    MaStrategy().run()
