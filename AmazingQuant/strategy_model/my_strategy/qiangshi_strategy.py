# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2024/1/4
# @Author  : gao
# @File    : qiangshi_strategy.py 
# @Project : AmazingQuant 
# ------------------------------
import time
import math

import numpy as np
import pandas as pd

from AmazingQuant.utils.performance_test import Timer
# import strategy基类
from AmazingQuant.strategy_center.strategy import *

# 取各种数据
from AmazingQuant.data_center.api_data.get_index_member import GetIndexMember
from AmazingQuant.factor_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.utils.logger import Logger
from AmazingQuant.environment import Environment
from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName


# 继承strategy基类
class MaStrategy(StrategyBase):
    def __init__(self, strategy_name='ma_strategy'):
        """
        用户定义类变量
        取本地数据
        :param strategy_name:
        """
        super().__init__(strategy_name=strategy_name)

        # 取指数成分股实例
        self.index_member_obj = GetIndexMember()
        # 取K线数据实例
        self.data_class = GetKlineData()
        # 取指标实例
        self.indicator = SaveGetIndicator()

        # 取指标数据
        self.now = time.time()
        Environment.logger = Logger(strategy_name)

    def initialize(self):
        # 设置运行模式，回测或者交易
        self.run_mode = RunMode.BACKTESTING.value
        # 设置回测资金账号
        self.account = ['test0']
        # 设置回测资金账号资金量
        self.capital = {'test0': 2000000}
        # 设置回测基准
        self.benchmark = '000300.SH'
        # 设置复权方式
        self.rights_adjustment = RightsAdjustment.FROWARD.value
        # 设置回测起止时间
        self.start = datetime(2013, 1, 1)
        self.end = datetime(2023, 7, 20)
        # 设置运行周期
        self.period = 'daily'
        self.index_member_obj.get_all_index_members()
        index_members_all = self.index_member_obj.get_index_members('000300.SH')
        print('index_members_all', len(index_members_all))

        # 选股结果
        factor_name = 'qiangshi'
        result_path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/' + factor_name + '/'
        self.qiangshi_result = get_local_data(result_path, factor_name+'.h5')
        self.universe = list(self.qiangshi_result.columns)

        # 设置在运行前是否缓存日线，分钟线等各个周期数据
        self.daily_data_cache = True
        Environment.logger.info(self.universe)

        # 回测滑点设置，按固定值0.01,20-0.01 = 19.99;百分比0.01,20*(1-0.01) = 19.98;平仓时用'+'
        self.set_slippage(stock_type=StockType.STOCK.value, slippage_type=SlippageType.SLIPPAGE_FIX.value, value=0.01)

        # 回测股票手续费和印花税，卖出印花税，千分之一；开仓手续费，万分之三；平仓手续费，万分之三，最低手续费，５元
        # 沪市，卖出有万分之二的过户费，加入到卖出手续费
        self.set_commission(stock_type=StockType.STOCK_SH.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.00032,
                            close_today_commission=0, min_commission=5)
        # 深市不加过户费
        self.set_commission(stock_type=StockType.STOCK_SZ.value, tax=0.001, open_commission=0.0003,
                            close_commission=0.0003,
                            close_today_commission=0, min_commission=5)

    def handle_bar(self, event):
        Environment.logger.info('self.time_tag', self.time_tag, Environment.bar_account_data_list[0]['total_balance'])
        Environment.logger.debug(len(Environment.bar_position_data_list))
        # 取当前bar的持仓情况
        with Timer(True):
            available_position_dict = {}
            for position in Environment.bar_position_data_list:
                available_position_dict[
                    position['instrument'] + '.' + position['exchange']] = position['position'] - position['frozen']

            close_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=self.universe,
                                                              field=['close'],
                                                              start=self.time_tag, end=self.time_tag)
            # print('close_price_all', close_price_all)

            open_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=self.universe,
                                                              field=['open'],
                                                              start=self.time_tag, end=self.time_tag)

            xuangu_result = self.qiangshi_result.loc[self.time_tag, :]
            xuangu_result = xuangu_result[xuangu_result==1]
            xuangu_result_list = list(xuangu_result.index)
            xuangu_result_num = len(xuangu_result_list)
            # 循环遍历股票池
            for stock in xuangu_result_list:
                # 取当前股票的收盘价
                open_price = open_price_all['open'][stock]
                if not open_price:
                    continue
                if math.isnan(open_price):
                    continue

                if stock not in available_position_dict.keys():
                    buy_shares = Environment.bar_account_data_list[0]['total_balance']/2/open_price/100/xuangu_result_num
                    buy_shares = int(buy_shares)*100
                    if buy_shares == 0:
                        Environment.logger.info('buy', stock, 'open_price:', open_price, '钱不够了')
                        continue
                    self.trade.order_shares(stock_code=stock, shares=buy_shares, price_type='fix',
                                            order_price=open_price,
                                            account_id=self.account[0])
                    Environment.logger.info('buy', stock, buy_shares, 'fix', open_price, self.account)

            for stock in available_position_dict.keys():
                if stock not in xuangu_result_list:
                    close_price = close_price_all['close'][stock]
                    Trade(self).order_shares(stock_code=stock, shares=-available_position_dict[stock], price_type='fix',
                                             order_price=close_price,
                                             account_id=self.account[0])
                    Environment.logger.info('sell not in xuangu_result', stock, -available_position_dict[stock], 'fix', close_price,
                                            self.account)
        self.now = time.time()


if __name__ == '__main__':
    # 测试运行完整个策略所需时间，沪深300动态股票池，一年数据，均线策略,10s完成,10S绩效分析
    with Timer(True):
        # 运行策略，设置是否保存委托，成交，资金，持仓
        ma_strategy = MaStrategy()
        ma_strategy.run(save_trade_record=True)
