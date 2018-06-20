# -*- coding: utf-8 -*-

__author__ = "gao"

import numpy as np
import talib

from AmazingQuant.strategy_center.strategy import *
# from AmazingQuant.environment import Environment
# import AmazingQuant.utils.data_transfer as data_transfer
# from AmazingQuant.data_center.get_data import GetData
# from AmazingQuant.constant import RunMode, Period, RightsAdjustment, ID
from AmazingQuant.trade_center.trade import Trade


class MaStrategy(StrategyBase):
    def initialize(self):
        self.run_mode = RunMode.BACKTESTING.value
        self.capital = 200000
        self.benchmark = "000002.SZ"
        self.start = "2005-01-08"
        self.end = "2005-02-28"
        self.period = "daily"
        self.universe = ["000002.SZ", "000001.SH"]
        self.daily_data_cache = True
        print(self.start)
        self.account = "test"

    def handle_bar(self, event):
        # print(self.benchmark)
        # print(self.timetag)
        current_date = data_transfer.millisecond_to_date(millisecond=self.timetag, format="%Y-%m-%d")
        current_date_int = data_transfer.date_str_to_int(current_date)
        data_class = GetData()
        close_price = data_class.get_market_data(Environment.daily_data, stock_code=["000002.SZ"], field=["close"],
                                                 start=self.start,
                                                 end=current_date)
        ma10 = talib.MA(np.array(close_price), timeperiod=10)
        ma30 = talib.MA(np.array(close_price), timeperiod=30)
        if ma10[-1] > ma30[-1]:
            # order_lots("000002.SZ",1,"fix",close_price[current_date_int],self.account)
            print("buy", 1, "fix", close_price[current_date_int], self.account)
        elif ma10[-1] < ma30[-1]:
            # order_lots("000002.SZ",1,"fix",close_price[current_date_int],self.account)
            print("sell", -1, "fix", close_price[current_date_int], self.account)
        Trade(self).order_lots(stock_code="000002.SZ", shares=10005, price_type="fix",
                                          order_price=close_price[current_date_int],
                                          account_id=self.account)
        # print(Environment.run_mode)

        # print(Environment.account[ID.ACCOUNT_ID], current_date)


if __name__ == "__main__":
    MaStrategy().run()
    # print(Environment.account)
    Environment.refresh()
    # print(Environment.account)
