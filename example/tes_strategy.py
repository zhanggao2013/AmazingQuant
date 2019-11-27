# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : tes_strategy.py.py
# @Project : AmazingQuant
# ------------------------------

import numpy as np
import talib
from datetime import datetime

# import strategy基类
from AmazingQuant.strategy_center.strategy import *

# import 交易模块
from AmazingQuant.trade_center.trade import Trade


# 继承strategy基类
class MaStrategy(StrategyBase):
    def initialize(self):
        # 设置运行模式，回测或者交易
        self.run_mode = RunMode.BACKTESTING.value
        # 设置回测资金账号
        self.account = ["test0", "test1"]
        # 设置回测资金账号资金量
        self.capital = {"test0": 2000000, "test1": 1000}
        # 设置回测基准
        self.benchmark = "600000.SH"
        # 设置复权方式
        self.rights_adjustment = RightsAdjustment.NONE.value
        # 设置回测起止时间
        self.start = datetime(2018, 1, 1)
        self.end = "2016-01-16"
        # 设置运行周期
        self.period = "daily"
        # 设置股票池
        self.universe = ['000001.SZ', '000002.SZ', '000008.SZ', '000060.SZ', '000063.SZ', '000069.SZ', '000100.SZ',
                         '000157.SZ', '000166.SZ', '000333.SZ', '000338.SZ', '000402.SZ', '000413.SZ', '000415.SZ',
                         '000423.SZ', '000425.SZ', '000503.SZ', '000538.SZ', '000540.SZ', '000559.SZ', '000568.SZ',
                         '000623.SZ', '000625.SZ', '000627.SZ', '000630.SZ', '000651.SZ', '000671.SZ', '000686.SZ',
                         '000709.SZ', '000723.SZ', '000725.SZ', '000728.SZ', '000738.SZ', '000750.SZ', '000768.SZ',
                         '000776.SZ', '000783.SZ', '000792.SZ', '000826.SZ', '000839.SZ', '000858.SZ', '000876.SZ',
                         '000895.SZ', '000898.SZ', '000938.SZ', '000959.SZ', '000961.SZ', '000963.SZ', '000983.SZ',
                         '001979.SZ', '002007.SZ', '002008.SZ', '002024.SZ', '002027.SZ', '002044.SZ', '002065.SZ',
                         '002074.SZ', '002081.SZ', '002142.SZ', '002146.SZ', '002153.SZ', '002174.SZ', '002202.SZ',
                         '002230.SZ', '002236.SZ', '002241.SZ', '002252.SZ', '002292.SZ', '002294.SZ', '002304.SZ',
                         '002310.SZ', '002352.SZ', '002385.SZ', '002411.SZ', '002415.SZ', '002424.SZ', '002426.SZ',
                         '002450.SZ', '002456.SZ', '002460.SZ', '002465.SZ', '002466.SZ', '002468.SZ', '002470.SZ',
                         '002475.SZ', '002500.SZ', '002508.SZ', '002555.SZ', '002558.SZ', '002572.SZ', '002594.SZ',
                         '002601.SZ', '002602.SZ', '002608.SZ', '002624.SZ', '002673.SZ', '002714.SZ', '002736.SZ',
                         '002739.SZ', '002797.SZ', '002831.SZ', '002839.SZ', '002841.SZ', '300003.SZ', '300015.SZ',
                         '300017.SZ', '300024.SZ', '300027.SZ', '300033.SZ', '300059.SZ', '300070.SZ', '300072.SZ',
                         '300122.SZ', '300124.SZ', '300136.SZ', '300144.SZ', '300251.SZ', '300315.SZ', '600000.SH',
                         '600008.SH', '600009.SH', '600010.SH', '600011.SH', '600015.SH', '600016.SH', '600018.SH',
                         '600019.SH', '600021.SH', '600023.SH', '600028.SH', '600029.SH', '600030.SH', '600031.SH',
                         '600036.SH', '600038.SH', '600048.SH', '600050.SH', '600061.SH', '600066.SH', '600068.SH',
                         '600074.SH', '600085.SH', '600089.SH', '600100.SH', '600104.SH', '600109.SH', '600111.SH',
                         '600115.SH', '600118.SH', '600153.SH', '600157.SH', '600170.SH', '600177.SH', '600188.SH',
                         '600196.SH', '600208.SH', '600219.SH', '600221.SH', '600233.SH', '600271.SH', '600276.SH',
                         '600297.SH', '600309.SH', '600332.SH', '600340.SH', '600352.SH', '600362.SH', '600369.SH',
                         '600372.SH', '600373.SH', '600376.SH', '600383.SH', '600390.SH', '600406.SH', '600415.SH',
                         '600436.SH', '600482.SH', '600485.SH', '600489.SH', '600498.SH', '600518.SH', '600519.SH',
                         '600522.SH', '600535.SH', '600547.SH', '600549.SH', '600570.SH', '600583.SH', '600585.SH',
                         '600588.SH', '600606.SH', '600637.SH', '600649.SH', '600660.SH', '600663.SH', '600674.SH',
                         '600682.SH', '600685.SH', '600688.SH', '600690.SH', '600703.SH', '600704.SH', '600705.SH',
                         '600739.SH', '600741.SH', '600795.SH', '600804.SH', '600816.SH', '600820.SH', '600827.SH',
                         '600837.SH', '600871.SH', '600886.SH', '600887.SH', '600893.SH', '600895.SH', '600900.SH',
                         '600909.SH', '600919.SH', '600926.SH', '600958.SH', '600959.SH', '600977.SH', '600999.SH',
                         '601006.SH', '601009.SH', '601012.SH', '601018.SH', '601021.SH', '601088.SH', '601099.SH',
                         '601111.SH', '601117.SH', '601118.SH', '601155.SH', '601163.SH', '601166.SH', '601169.SH',
                         '601186.SH', '601198.SH', '601211.SH', '601212.SH', '601216.SH', '601225.SH', '601228.SH',
                         '601229.SH', '601288.SH', '601318.SH', '601328.SH', '601333.SH', '601336.SH', '601375.SH',
                         '601377.SH', '601390.SH', '601398.SH', '601555.SH', '601600.SH', '601601.SH', '601607.SH',
                         '601608.SH', '601611.SH', '601618.SH', '601628.SH', '601633.SH', '601668.SH', '601669.SH',
                         '601688.SH', '601718.SH', '601727.SH', '601766.SH', '601788.SH', '601800.SH', '601818.SH',
                         '601857.SH', '601866.SH', '601872.SH', '601877.SH', '601878.SH', '601881.SH', '601888.SH',
                         '601898.SH', '601899.SH', '601901.SH', '601919.SH', '601933.SH', '601939.SH', '601958.SH',
                         '601966.SH', '601985.SH', '601988.SH', '601989.SH', '601991.SH', '601992.SH', '601997.SH',
                         '601998.SH', '603160.SH', '603799.SH', '603833.SH', '603858.SH', '603993.SH']

        # 设置在运行前是否缓存日线，分钟线等各个周期数据
        self.daily_data_cache = True
        print(self.universe)

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

    def handle_bar(self, event):
        print(self.timetag)
        # 取当前bar的持仓情况
        available_position_dict = {}
        for position in Environment.bar_position_data_list:
            available_position_dict[position.instrument + "." + position.exchange] = position.position - position.frozen
        # 当前bar的具体时间戳
        # current_date = data_transfer.millisecond_to_date(millisecond=self.timetag, format="%Y-%m-%d")
        # 时间戳转换成int，方便后面取数据
        # current_date_int = data_transfer.date_str_to_int(current_date)
        # print(current_date)
        # 取数据实例
        data_class = GetKlineData()
        # 循环遍历股票池
        for stock in self.universe:
            # 取当前股票的收盘价
            close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock], field=["close"],
                                                     end=self.timetag)
            # print(self.start, current_date)
            close_array = np.array(close_price)
            print(stock, close_array)
            if len(close_array) > 0:
                # 利用talib计算MA
                ma5 = talib.MA(np.array(close_price), timeperiod=5)
                ma20 = talib.MA(np.array(close_price), timeperiod=20)
                # print(type(close_price.keys()))
                # 过滤因为停牌没有数据
                if current_date_int in close_price.keys():
                    # 如果5日均线突破20日均线，并且没有持仓，则买入这只股票100股，以收盘价为指定价交易
                    if ma5[-1] > ma20[-1] and stock not in available_position_dict.keys():
                        Trade(self).order_shares(stock_code=stock, shares=100, price_type="fix",
                                                 order_price=close_price[current_date_int],
                                                 account=self.account[0])
                        print("buy", stock, 1, "fix", close_price[current_date_int], self.account)
                    # 如果20日均线突破5日均线，并且有持仓，则卖出这只股票100股，以收盘价为指定价交易
                    elif ma5[-1] < ma20[-1] and stock in available_position_dict.keys():
                        Trade(self).order_shares(stock_code=stock, shares=-100, price_type="fix",
                                                 order_price=close_price[current_date_int],
                                                 account=self.account[0])
                        print("sell", stock, -1, "fix", close_price[current_date_int], self.account)


if __name__ == "__main__":
    # 测试运行完整个策略所需时间
    from AmazingQuant.utils.performance_test import Timer

    time_test = Timer(True)
    with time_test:
        # 运行策略，设置是否保存委托，成交，资金，持仓
        MaStrategy().run(save_trade_record=False)
