# AmazingQuant<br>
[![Github workers](https://img.shields.io/github/watchers/zhanggao2013/AmazingQuant.svg?style=social&label=Watchers&)](https://github.com/zhanggao2013/AmazingQuant/watchers)
[![GitHub stars](https://img.shields.io/github/stars/zhanggao2013/AmazingQuant.svg?style=social&label=Star&)](https://github.com/zhanggao2013/AmazingQuant/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zhanggao2013/AmazingQuant.svg?style=social&label=Fork&)](https://github.com/zhanggao2013/AmazingQuant/fork)

# 1.简介
AmazingQuant是一款基于event-driven的量化回测交易开源框架，下图是总体框架架构。
![](https://github.com/zhanggao2013/AmazingQuant/raw/master/documents/framework_architecture.jpg)  
* data_center
    * to_mongoDB 存放行情、财务等各种数据到MongoDB的存储模块
    * get_data   策略中从数据库中取数据的接口模块
* trade_center
    * mossion_engine   包含下单任务（event_order）和风控（event_risk_management）两部分的engine，分别完成下单前的检查和风控
    * broker_engine    分为回测时的simulate的broker（主要是event_deal）撮合成交和连接实盘交易CTP、xSpeed等接口两部分
* strategy_center
    * bar_engine       在回测或者交易模式下，用`逐K线`的方式执行每一根bar的交易逻辑，可在日线、分钟线、分笔下运行
* analysis_center
    * analysis_engine  对回测形成的交易记录进行分析和可视化，净值、年化收益、alpha、beta、回撤等指标，brison、Fama等经典模型的实现

# 2.安装配置
* MongoDB 3.4 <br> 
      建议使用shard，[配置启动项示例](https://github.com/zhanggao2013/AmazingQuant/blob/master/documents/MongoDB_config.md)
* pymongo <br> 
      python调用MongoDB
* talib <br> 
      技术指标计算库
* anaconda <br> 
      python 3.5 的版本，如果大于3.5的版本，ctp的接口暂时不能用，因为编译问题，后续可以解决
* Linux Ubuntu <br> 
      开发环境是ubuntu，当然也可以在windows下用，但是数据库的配置和ctp等交易接口需要重新做
* 安装AmazingQuant
      pip install AmazingQuant  直接安装

# 3.策略编写
```python
# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : example_strategy.py.py
# @Project : AmazingQuant
# ------------------------------

import time
import numpy as np
import pandas as pd
import talib
from datetime import datetime

from AmazingQuant.utils.performance_test import Timer
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
        # 取指数成分股实例
        self.index_member_obj = GetIndexMember()
        # 取K线数据实例
        self.data_class = GetKlineData()

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
        print('self.time_tag', self.time_tag, datetime.now())
        # 取当前bar的持仓情况
        with Timer(True):
            available_position_dict = {}
            for position in Environment.bar_position_data_list:
                available_position_dict[position.instrument + '.' + position.exchange] = position.position - position.frozen
            index_member_list = self.index_member_obj.get_index_member_in_date(self.time_tag)

            close_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=self.universe, field=['close'],
                                                              start=self.start, end=self.time_tag)
            # 循环遍历股票池
            for stock in self.universe:
                # 取当前股票的收盘价
                close_price = close_price_all['close'][stock]
                close_array = np.array(close_price)

                if len(close_array) > 0:
                    # 利用talib计算MA
                    try:
                        ma5 = talib.MA(close_array[-20:], timeperiod=5)
                        ma20 = talib.MA(close_array[-20:], timeperiod=20)
                    except Exception as e:
                        continue

                    # print('ma5', ma5[-1], ma20[-1], ma5[-1] > ma20[-1], len(available_position_dict.keys()))

                    # 过滤因为停牌没有数据
                    if self.time_tag in close_price.index:
                        # 如果5日均线突破20日均线，并且没有持仓，则买入这只股票100股，以收盘价为指定价交易
                        if ma5[-1] > ma20[-1] and stock not in available_position_dict.keys() and stock in index_member_list:
                            Trade(self).order_shares(stock_code=stock, shares=100, price_type='fix',
                                                     order_price=close_price.loc[self.time_tag],
                                                     account=self.account[0])
                            print('buy', stock, -1, 'fix', close_price.loc[self.time_tag], self.account)
                        # 如果20日均线突破5日均线，并且有持仓，则卖出这只股票100股，以收盘价为指定价交易
                        elif ma5[-1] < ma20[-1] and stock in available_position_dict.keys():
                            Trade(self).order_shares(stock_code=stock, shares=-100, price_type='fix',
                                                     order_price=close_price.loc[self.time_tag],
                                                     account=self.account[0])
                            print('sell', stock, -1, 'fix', close_price.loc[self.time_tag], self.account)
                        elif stock in available_position_dict.keys() and stock not in index_member_list:
                            Trade(self).order_shares(stock_code=stock, shares=-100, price_type='fix',
                                                     order_price=close_price.loc[self.time_tag],
                                                     account=self.account[0])
                            print('sell not in index_member_list', stock, -1, 'fix', close_price.loc[self.time_tag], self.account)


if __name__ == '__main__':
    # 测试运行完整个策略所需时间，沪深300动态股票池，一年数据，均线策略
    with Timer(True):
        # 运行策略，设置是否保存委托，成交，资金，持仓
        ma_strategy = MaStrategy()
        ma_strategy.run(save_trade_record=True)

```
# 4.回测结果分析
* 自动生成回测结果<br>
产生的[委托](https://github.com/zhanggao2013/AmazingQuant/blob/master/example/test_strategy_order_data1530494369000.csv)，[成交](https://github.com/zhanggao2013/AmazingQuant/blob/master/example/test_strategy_deal_data1530494369000.csv)，[资金](https://github.com/zhanggao2013/AmazingQuant/blob/master/example/test_strategy_account_data1530494369000.csv)，[持仓](https://github.com/zhanggao2013/AmazingQuant/blob/master/example/test_strategy_position_data1530494369000.csv)的cvs文件写入到策略所在文件夹
* 自动生成回测报告<br>
[回测报告](https://github.com/zhanggao2013/AmazingQuant/blob/master/example/test_strategy_strategy%20backtesting%20indicator1530494371000.html)是html格式，可在浏览器中打开查看，效果如下图： 
![](https://github.com/zhanggao2013/AmazingQuant/raw/master/documents/backtesting_result.jpg)  
# 5.已实现和即将实现的功能
* 已实现
   * 数据库搭建
   * 读取数据
   * 策略运行回测
   * 回测交易记录的保存和分析
   * 实盘CTP接口的封装
* 即将实现
   * 各种数据的对接<br>
   例如股票的分钟数据、股票财务数据、股票板块成分股、期货分钟数据、日线数据等
   * CTP等交易接口与broker_engine对接<br>
   CTP、xSpeed等
   * 对回测区间的每一根bar的交易和持仓情况可视化<br>
   * 回测分析模块的丰富<br>
   增加brison、FAMA等各种绩效归因模型的分析和可视化
      
# 6.联系方式
欢迎加qq群讨论: 788279189 [qq群链接](https://jq.qq.com/?_wv=1027&k=5gK6IDW) <br>
我的qq：37475036
