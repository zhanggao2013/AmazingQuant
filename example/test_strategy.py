# -*- coding: utf-8 -*-

__author__ = "gao"

import numpy as np
import talib

from AmazingQuant.strategy_center.strategy import *
from AmazingQuant.trade_center.trade import Trade


class MaStrategy(StrategyBase):
    def initialize(self):
        self.run_mode = RunMode.BACKTESTING.value
        self.capital = {"test0": 2000000000, "test1":1000}
        self.benchmark = "000002.SZ"
        self.start = "2005-01-08"
        self.end = "2005-01-28"
        self.period = "daily"
        self.universe = ["000002.SZ", "000001.SH"]
        self.daily_data_cache = True
        print(self.start)
        self.account = ["test0", "test1"]

        # 回测滑点设置，按固定值0.01,20-0.01 = 19.99;百分比0.01,20*(1-0.01) = 19.98;平仓时用"+"
        self.set_slippage(stock_type=StockType.STOCK.value, slippage_type=SlippageType.SLIPPAGE_FIX.value, value=0.01)

        # 回测股票手续费和印花税，卖出印花税，千分之一；开仓手续费，万分之三；平仓手续费，万分之三，最低手续费，５元
        # 沪市，卖出有万分之二的过户费，加入到卖出手续费
        self.set_commission(stock_type=StockType.STOCK_SH.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.0003,
                            close_today_commission=0, min_commission=5)
        # 深市不加过户费
        self.set_commission(stock_type=StockType.STOCK_SZ.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.0005,
                            close_today_commission=0, min_commission=5)
        print(Environment.slippage_dict)

        print(Environment.commission_dict)

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
        Trade(self).order_lots(stock_code="000002.SZ", shares=100, price_type="fix",
                               order_price=close_price[current_date_int],
                               account=self.account[0])
        if self.bar_index > 5:
            Trade(self).order_lots(stock_code="000002.SZ", shares=-100, price_type="fix",
                                   order_price=close_price[current_date_int],
                                   account=self.account[1])

        print(len(Environment.bar_position_data_list))
        for position in Environment.bar_position_data_list:
            print(position.instrument + "" + position.exchange)
            print(position.position)

        # print(Environment.account[ID.ACCOUNT_ID], current_date)


if __name__ == "__main__":
    MaStrategy().run()
    # print(Environment.account)
