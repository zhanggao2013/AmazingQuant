# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : example_strategy.py.py
# @Project : AmazingQuant
# ------------------------------
import time

from AmazingQuant.utils.performance_test import Timer
# import strategy基类
from AmazingQuant.strategy_center.strategy import *

# 取各种数据
from AmazingQuant.data_center.api_data.get_index_member import GetIndexMember
from AmazingQuant.factor_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.utils.logger import Logger
from AmazingQuant.environment import Environment


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
        self.ma5 = self.indicator.get_indicator('ma5')
        self.ma10 = self.indicator.get_indicator('ma10')
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
        self.start = datetime(2018, 1, 1)
        self.end = datetime(2019, 1, 1)
        # 设置运行周期
        self.period = 'daily'
        self.index_member_obj.get_all_index_members()
        index_members_all = self.index_member_obj.get_index_members('000300.SH')
        print('index_members_all', len(index_members_all))
        self.universe = index_members_all

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
        Environment.logger.info('self.time_tag', self.time_tag, datetime.now(), (time.time() - self.now) * 1000)
        Environment.logger.debug(len(Environment.bar_position_data_list))
        # 取当前bar的持仓情况
        with Timer(True):
            available_position_dict = {}
            for position in Environment.bar_position_data_list:
                available_position_dict[
                    position['instrument'] + '.' + position['exchange']] = position['position'] - position['frozen']
            index_member_list = self.index_member_obj.get_index_member_in_date(self.time_tag, index_code=self.benchmark)
            print('index_member_list', len(index_member_list))
            close_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=self.universe,
                                                              field=['close'],
                                                              start=self.time_tag, end=self.time_tag)
            # print('close_price_all', close_price_all)
            # 循环遍历股票池
            for stock in index_member_list:
                # 取当前股票的收盘价
                close_price = close_price_all['close'][stock]
                if not close_price:
                    continue
                if not((stock in self.ma5) and (stock in self.ma10)):
                    continue
                ma5 = self.ma5[stock][self.time_tag]
                ma20 = self.ma10[stock][self.time_tag]
                if ma5 and ma20:
                    # 如果5日均线突破20日均线，并且没有持仓，则买入这只股票100股，以收盘价为指定价交易
                    if ma5 > ma20 and stock not in available_position_dict.keys() and stock in index_member_list:
                        self.trade.order_shares(stock_code=stock, shares=100, price_type='fix',
                                                order_price=close_price,
                                                account_id=self.account[0])
                        Environment.logger.info('buy', stock, -1, 'fix', close_price, self.account)
                    # 如果20日均线突破5日均线，并且有持仓，则卖出这只股票100股，以收盘价为指定价交易
                    elif ma5 < ma20 and stock in available_position_dict.keys():
                        self.trade.order_shares(stock_code=stock, shares=-100, price_type='fix',
                                                order_price=close_price,
                                                account_id=self.account[0])
                        Environment.logger.info('sell', stock, -1, 'fix', close_price, self.account)
            for stock in available_position_dict.keys():
                if stock not in index_member_list:
                    close_price = close_price_all['close'][stock]
                    Trade(self).order_shares(stock_code=stock, shares=-100, price_type='fix',
                                             order_price=close_price,
                                             account_id=self.account[0])
                    Environment.logger.info('sell not in index_member_list', stock, -1, 'fix', close_price,
                                            self.account)
        self.now = time.time()


if __name__ == '__main__':
    # 测试运行完整个策略所需时间，沪深300动态股票池，一年数据，均线策略,10s完成,10S绩效分析
    with Timer(True):
        # 运行策略，设置是否保存委托，成交，资金，持仓
        ma_strategy = MaStrategy()
        ma_strategy.run(save_trade_record=True)
