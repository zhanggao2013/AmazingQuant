# AmazingQuant<br>
[![Github workers](https://img.shields.io/github/watchers/zhanggao2013/AmazingQuant.svg?style=social&label=Watchers&)](https://github.com/zhanggao2013/AmazingQuant/watchers)
[![GitHub stars](https://img.shields.io/github/stars/zhanggao2013/AmazingQuant.svg?style=social&label=Star&)](https://github.com/zhanggao2013/AmazingQuant/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zhanggao2013/AmazingQuant.svg?style=social&label=Fork&)](https://github.com/zhanggao2013/AmazingQuant/fork)

# 1.简介
AmazingaQuant——为交易而生的智能投研Lab。包含策略模型研究服务、量化数据服务、指标计算服务、绩效分析服务四大功能模块。	<br/>
1.1 策略研究服务	<br/>
　　四大策略体系的研究体系<br/>
（1）选股体系<br/>
　　中低频组合选股模型、强势短线模型<br/>
（2）风险预警体系<br/>
　　事件风险等建立黑白名单模型<br/>
（3）择时体系<br/>
　　仓位控制择时、行业风格轮动<br/>
（4）T+0体系<br/>
　  全市场股票分类（活跃型与稳定型），做T0模型	<br/>

1.2 量化数据服务	<br/>
1.2.1 历史数据存储	<br/>
存储到服务器的mongoDB作为数据服务器，并保存到本地的HDF5，满足策略需求。	<br/>
（1）基础行情数据	<br/>
　　tick、1min、5min、日线等周期的股票、指数	<br/>
（2）基本面数据	<br/>
　　财务数据	<br/>
　　股本数据	<br/>
（3）行情衍生数据	<br/>
　　龙虎榜数据	<br/>
　　指数成分股数据	<br/>
　　行业板块成分股数据	<br/>
　　行业指数日线行情数据	<br/>

1.2.1  实时行情对接	<br/>
（1）股票、指数的tick数据实时全推行情	<br/>
（2）重采样为1min、5min、日线等三个周期数据	<br/>

1.3 指标计算服务	<br/>
　　历史指标计算满足策略研究，实时指标计算满足实盘交易<br/>
（1）日线、周线、月线、年线周期等低频指标的历史数据计算，固定存储为HDF5格式，	<br/>
（2）分钟、tick周期等高频数据指标计算，历史数据计算和实时指标计算两部分	<br/>

1.4 绩效分析服务	<br/>
　　回测数据格式对接，满足策略研究的评价；实盘数据格式对接，满足实盘运行的监控。	<br/>
1.4.1 净值数据分析	<br/>
（1）年化波动率,日收益波动率,月收益波动率，该值表明因子对收益率贡献的波动程度	<br/>
（2）日收益率分布,月收益率分布,正收益天数,负收益天数,日胜率,月胜率,峰度,偏度	<br/>
（3）最大回撤	<br/>
（4）夏普比率,calmar比率,特雷诺比率,索提诺比率	<br/>
（5）beta,跟踪误差,信息比率	<br/>
1.4.2 交易数据分析	<br/>
（1）也针对回测的：滑点损失	<br/>
（2）总交易次数、日均交易次数、胜率（个股从建仓到完全平仓）、平均持仓周期、换手率、交易费用、总交易金额	<br/>
（3）分每只股票统计，交易数量、金额、时间	<br/>
1.4.3 持仓数据分析	<br/>
（1）持仓行业市值、占比	<br/>
（2）持仓估值风格分析	<br/>
（3）持仓综合风格分析	<br/>
1.4.4 绩效归因	<br/>
（1）多因子归因	<br/>
　　投资收益分为每个风格（行业）因子收益、特殊收益、日内调仓收益 <br/>
（2）brinson归因	<br/>
　　投资收益分为基准收益和超额收益，其中超额收益分为：资产配置收益、个股选择收益和交互收益<br/>
（3）收益分解	<br/>
　　市场中性策略,基本分解公式为：总收益=交易收益+选股收益+择时收益+基差收益+交易成本	<br/>
　　纯股票策略,基本分解公式为：总收益=交易收益+选股收益+择时收益+基准收益+交易成本	<br/>
    
下图是总体框架架构。	<br/>
![](https://github.com/zhanggao2013/AmazingQuant/blob/master/documents/framework_architecture.jpg)
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
#-*- coding: utf-8 -*-

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
from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator
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
        _, index_members_all = self.index_member_obj.get_index_members('000300.SH')
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
                    position.instrument + '.' + position.exchange] = position.position - position.frozen
            index_member_list = self.index_member_obj.get_index_member_in_date(self.time_tag)

            close_price_all = self.data_class.get_market_data(Environment.daily_data, stock_code=index_member_list,
                                                              field=['close'],
                                                              start=self.time_tag, end=self.time_tag)
            # 循环遍历股票池
            for stock in index_member_list:
                # 取当前股票的收盘价
                close_price = close_price_all['close'][stock]
                if close_price:
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

```
 
# 4.联系方式
qq群:：<br>
     788279189 [qq群链接](https://jq.qq.com/?_wv=1027&k=5gK6IDW) <br>
知识星球:：<br>
      ![](https://github.com/zhanggao2013/AmazingQuant/blob/master/documents/starGitHub.jpg)<br>
微信公众号：<br>
                    ![](https://github.com/zhanggao2013/AmazingQuant/blob/master/documents/wechat.jpg)
