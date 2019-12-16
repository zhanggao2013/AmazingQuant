# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : example_strategy.py.py
# @Project : AmazingQuant
# ------------------------------

import numpy as np
import pandas as pd
import talib
from datetime import datetime

# import strategy基类
from AmazingQuant.strategy_center.strategy import *

# import 交易模块
from AmazingQuant.trade_center.trade import Trade

# 取各种数据
from AmazingQuant.data_center.get_data.get_index_member import GetIndexMember


# 继承strategy基类
class MaStrategy(StrategyBase):
    def __init__(self):
        super().__init__()
        self.index_member_obj = GetIndexMember()

    def initialize(self):
        # 设置运行模式，回测或者交易
        self.run_mode = RunMode.BACKTESTING.value
        # 设置回测资金账号
        self.account = ['test0', 'test1']
        # 设置回测资金账号资金量
        self.capital = {'test0': 2000000, 'test1': 1000}
        # 设置回测基准
        self.benchmark = '000300.SH'
        # 设置复权方式
        self.rights_adjustment = RightsAdjustment.NONE.value
        # 设置回测起止时间
        self.start = datetime(2018, 1, 1)
        self.end = datetime(2019, 1, 1)
        # 设置运行周期
        self.period = 'daily'
        _, index_members_all = self.index_member_obj.get_index_members('000300.SH')
        self.universe = index_members_all

        # 设置在运行前是否缓存日线，分钟线等各个周期数据
        self.daily_data_cache = True
        print(self.universe)

        # 回测滑点设置，按固定值0.01,20-0.01 = 19.99;百分比0.01,20*(1-0.01) = 19.98;平仓时用'+'
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

    def handle_bar(self, event):
        print('self.timetag', self.timetag)
        # 取当前bar的持仓情况
        available_position_dict = {}
        for position in Environment.bar_position_data_list:
            available_position_dict[position.instrument + '.' + position.exchange] = position.position - position.frozen
        index_member_list = self.index_member_obj.get_index_member_in_date(self.timetag)
        # 取数据实例
        data_class = GetKlineData()
        # 循环遍历股票池
        for stock in self.universe:
            # 取当前股票的收盘价
            close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock], field=['close'],
                                                     start=self.start, end=self.timetag)
            # print(close_price)
            close_array = np.array(close_price.dropna())
            # print(stock,  close_price.index)
            if len(close_array) > 0:
                # 利用talib计算MA
                ma5 = talib.MA(close_array[-20:], timeperiod=5)
                ma20 = talib.MA(close_array[-20:], timeperiod=20)

                # print('ma5', ma5[-1], ma20[-1], ma5[-1] > ma20[-1], len(available_position_dict.keys()))

                # 过滤因为停牌没有数据
                if self.timetag in close_price.index:
                    # 如果5日均线突破20日均线，并且没有持仓，则买入这只股票100股，以收盘价为指定价交易
                    if ma5[-1] > ma20[-1] and stock not in available_position_dict.keys() and stock in index_member_list:
                        Trade(self).order_shares(stock_code=stock, shares=100, price_type='fix',
                                                 order_price=close_price.loc[self.timetag],
                                                 account=self.account[0])
                        print('buy', stock, -1, 'fix', close_price.loc[self.timetag], self.account)
                    # 如果20日均线突破5日均线，并且有持仓，则卖出这只股票100股，以收盘价为指定价交易
                    elif ma5[-1] < ma20[-1] and stock in available_position_dict.keys():
                        Trade(self).order_shares(stock_code=stock, shares=-100, price_type='fix',
                                                 order_price=close_price.loc[self.timetag],
                                                 account=self.account[0])
                        print('sell', stock, -1, 'fix', close_price.loc[self.timetag], self.account)
                    elif stock in available_position_dict.keys() and stock not in index_member_list:
                        Trade(self).order_shares(stock_code=stock, shares=-100, price_type='fix',
                                                 order_price=close_price.loc[self.timetag],
                                                 account=self.account[0])
                        print('sell not in index_member_list', stock, -1, 'fix', close_price.loc[self.timetag], self.account)


if __name__ == '__main__':
    # 测试运行完整个策略所需时间
    from AmazingQuant.utils.performance_test import Timer
    with Timer(True):
        # 运行策略，设置是否保存委托，成交，资金，持仓
        ma_strategy = MaStrategy()
        ma_strategy.run(save_trade_record=True)
