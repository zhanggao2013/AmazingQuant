# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : stratification_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
分层法
（1）根据因子排序分组，
（2）每组持仓股票作为策略，进入回测模块分析
"""
import time

import pandas as pd
import numpy as np

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data

# import strategy基类
from AmazingQuant.strategy_center.strategy import *

# import 交易模块
from AmazingQuant.trade_center.trade import Trade

from AmazingQuant.utils.logger import Logger
from AmazingQuant.environment import Environment


class StratificationAnalysis(object):
    def __init__(self, factor, factor_name, group_num=5):
        self.factor = factor
        self.factor_name = factor_name
        self.group_num = group_num
        self.factor_group = None
        self.group_key = ['group_' + str(i) for i in range(group_num)]

    def add_group(self, ascending=True):
        factor_rank = self.factor.rank(axis=1, ascending=ascending)
        self.factor_group = factor_rank.apply(lambda x: pd.cut(x, self.group_num, labels=self.group_key), axis=1)

    def cal_group_hold(self, group_name):
        return self.factor_group[self.factor_group == group_name]


# 继承strategy基类
class StratificationStrategy(StrategyBase):
    def __init__(self, group_hold, strategy_name='stratification_strategy'):
        """
        用户定义类变量
        取本地数据
        :param strategy_name:
        """
        super().__init__(strategy_name=strategy_name)

        # 取K线数据实例
        self.data_class = GetKlineData()
        self.group_hold = group_hold
        self.group_hold_index = self.group_hold.index
        self.single_stock_value = None

        # 初始仓位，因交易费用，满仓后无法慢如
        self.hold_ratio = 0.95
        self.group_hold_num = self.group_hold.iloc[0].dropna().shape[0]
        Environment.logger = Logger(strategy_name)

    def initialize(self):
        # 设置运行模式，回测或者交易
        self.run_mode = RunMode.BACKTESTING.value
        # 设置回测资金账号
        self.account = ['test0']
        # 设置回测资金账号资金量
        self.capital = {'test0': 100000000}
        # 设置回测基准
        self.benchmark = '000300.SH'
        # 设置复权方式
        self.rights_adjustment = RightsAdjustment.FROWARD.value
        # 设置回测起止时间
        self.start = self.group_hold.index[0]
        # self.start = datetime(2019, 12, 5)
        self.end = self.group_hold.index[-1]
        # 设置运行周期
        self.period = 'daily'

        # 设置在运行前是否缓存日线，分钟线等各个周期数据
        self.daily_data_cache = True
        Environment.logger.info(self.universe)

        # 回测滑点设置，按固定值0.01,20-0.01 = 19.99;百分比0.01,20*(1-0.01) = 19.98;平仓时用'+'
        self.set_slippage(stock_type=StockType.STOCK.value, slippage_type=SlippageType.SLIPPAGE_FIX.value, value=0.01)

        # 回测股票手续费和印花税，卖出印花税，千分之一；开仓手续费，万分之三；平仓手续费，万分之三，最低手续费，５元
        # 沪市，卖出有十万分之二的过户费，加入到卖出手续费
        self.set_commission(stock_type=StockType.STOCK_SH.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.00032,
                            close_today_commission=0, min_commission=5)
        # 深市不加过户费
        self.set_commission(stock_type=StockType.STOCK_SZ.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.0003,
                            close_today_commission=0, min_commission=5)

        self.single_stock_value = self.capital[self.account[0]] * self.hold_ratio / self.group_hold_num

    def handle_bar(self, event):
        Environment.logger.info('self.time_tag', self.time_tag, datetime.now())
        # Environment.logger.debug(len(Environment.bar_position_data_list))
        if self.time_tag not in self.group_hold_index:
            return

        # 取当前bar的持仓情况
        available_position_dict = {}
        for position in Environment.bar_position_data_list:
            if position.account_id == self.account[0]:
                available_position_dict[position.instrument + '.' + position.exchange] = position.position - position.frozen

        # 因子选股的持仓股票
        current_group_hold_list = self.group_hold.loc[self.time_tag].dropna().index.values
        # 当前资金账户的持仓股票
        position_stock_list = list(available_position_dict.keys())
        # 需要买入调仓的股票
        buy_stock_list = np.setdiff1d(current_group_hold_list, position_stock_list)
        # 需要卖出调仓的股票
        sell_stock_list = np.setdiff1d(position_stock_list, current_group_hold_list)
        # 需要调仓的股票，取这些票的收盘价
        buy_sell_stock_list = np.union1d(buy_stock_list, sell_stock_list)
        close_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=buy_sell_stock_list,
                                                          field=['close'],
                                                          start=self.time_tag, end=self.time_tag)

        Environment.logger.info(len(current_group_hold_list), len(position_stock_list), len(buy_stock_list),
                                len(sell_stock_list))

        print(Environment.bar_account_data_list[0].available)
        # 循环遍历股票池
        for stock in sell_stock_list:
            # 取当前股票的收盘价
            close_price = close_price_all['close'][stock]
            if np.isnan(close_price):
                continue
            Trade(self).order_shares(stock_code=stock, shares=-available_position_dict[stock], price_type='fix',
                                     order_price=close_price, account_id=self.account[0])
            Environment.logger.info(self.time_tag, 'sell', stock, available_position_dict[stock],
                                    'fix', close_price, self.account[0])

        print(Environment.bar_account_data_list[0].available, Environment.bar_account_data_list[0].account_id)
        # print(position_stock_list)
        if position_stock_list:
            self.single_stock_value = (Environment.bar_account_data_list[0].available -
                                       Environment.bar_account_data_list[0].total_balance * (1 - self.hold_ratio)) / \
                                      len(buy_stock_list)
            self.single_stock_value = max(self.single_stock_value, 0)
            print(self.single_stock_value)

        if self.single_stock_value > 0:
            for stock in buy_stock_list:
                # 取当前股票的收盘价
                close_price = close_price_all['close'][stock]
                if np.isnan(close_price):
                    continue
                buy_share = int(self.single_stock_value / close_price / 100) * 100
                Trade(self).order_shares(stock_code=stock, shares=buy_share, price_type='fix', order_price=close_price,
                                         account_id=self.account[0])
                Environment.logger.info(self.time_tag, 'buy', stock, buy_share, 'fix', close_price, self.account[0])


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma5 = factor_ma5[factor_ma5.index < datetime(2020, 1, 1)]
    stratification_analysis_obj = StratificationAnalysis(factor_ma5, 'factor_ma5')
    stratification_analysis_obj.add_group()
    group_hold = stratification_analysis_obj.cal_group_hold(stratification_analysis_obj.group_key[0])
    stratification_strategy = StratificationStrategy(group_hold)
    import time

    a = time.time()
    stratification_strategy.run(save_trade_record=True)
    print(time.time() - a)
