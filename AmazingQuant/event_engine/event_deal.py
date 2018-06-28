# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event
from AmazingQuant.environment import Environment
from AmazingQuant.data_center.get_data import GetData
from AmazingQuant.constant import *
from AmazingQuant.utils.generate_random_id import generate_random_id


class EventDeal(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_DEAL.value)

    @classmethod
    def initialize_deal_data(cls, event):
        # 　代码编号相关
        # self.trade_id = Empty.EMPTY_STRING.value  # 成交编号
        # self.instrument = Empty.EMPTY_STRING.value  # 合约代码
        # self.exchange = Empty.EMPTY_STRING.value  # 交易所代码
        # self.order_id = Empty.EMPTY_STRING.value  # 订单编号

        # 　成交相关
        # self.deal_price = Empty.EMPTY_FLOAT.value  # 成交价格
        # self.direction = Empty.EMPTY_STRING.value  # 成交方向
        # self.offset = Empty.EMPTY_STRING.value  # 成交开平
        # self.deal_volume = Empty.EMPTY_INT.value  # 成交数量
        # self.deal_time = Empty.EMPTY_STRING.value  # 成交时间
        if Environment.current_order_data.status == Status.NOT_TRADED.value:
            Environment.current_deal_data.trade_id = generate_random_id(topic=ID.DEAL_ID.value)
            Environment.current_deal_data.instrument = Environment.current_order_data.instrument
            Environment.current_deal_data.exchange = Environment.current_order_data.exchange
            Environment.current_deal_data.order_id = Environment.current_order_data.order_id

            Environment.current_deal_data.deal_price = Environment.current_order_data.order_price
            Environment.current_deal_data.offset = Environment.current_order_data.offset
            Environment.current_deal_data.deal_volume = Environment.current_order_data.total_volume
            Environment.current_deal_data.deal_time = Environment.current_order_data.order_time

    @classmethod
    def slippage_calculate(cls, event):
        """
        根据滑点设定，　计算成交价格
        :param event:
        :return:
        """
        if Environment.current_deal_data.exchange == "SH" or Environment.current_deal_data.exchange == "SZ":

            if Environment.slippage_dict[StockType.STOCK.value]["slippage_type"] == SlippageType.SLIPPAGE_FIX.value:

                if Environment.current_deal_data.offset == Offset.OPEN.value:
                    Environment.current_deal_data.deal_price += \
                        Environment.slippage_dict[StockType.STOCK.value]["value"]
                    print("slippage_calculate")
                elif Environment.current_deal_data.offset == Offset.CLOSE.value:
                    Environment.current_deal_data.deal_price -= \
                        Environment.slippage_dict[StockType.STOCK.value]["value"]

            elif Environment.slippage_dict[StockType.STOCK.value]["slippage_type"] == \
                    SlippageType.SLIPPAGE_PERCENT.value:
                if Environment.current_deal_data.offset == Offset.OPEN.value:
                    Environment.current_deal_data.deal_price *= (
                            1 + Environment.slippage_dict[StockType.STOCK.value]["value"])

                elif Environment.current_deal_data.offset == Offset.CLOSE.value:
                    Environment.current_deal_data.deal_price *= (
                            1 - Environment.slippage_dict[StockType.STOCK.value]["value"])
        else:
            # 期货品种滑点计算后续补充
            pass

    @classmethod
    def commission_calculate(cls, event):
        """
        根据手续费设定，更新成交价格
        :param event:
        :return:
        """
        # set_commission(self, stock_type=StockType.STOCK.value, tax=0, open_commission=0, close_commission=0,
        #                close_today_commission=0, min_commission=0):
        # Environment.commission_dict[stock_type] = {"tax": tax, "open_commission": open_commission,
        #                                            "close_commission": close_commission,
        #                                            "close_today_commission": close_today_commission,
        #                                            "min_commission": min_commission}
        commission = {}
        trade_balance = Environment.current_deal_data.deal_price * Environment.current_deal_data.deal_volume
        # 分市场标的计算手续费率
        if Environment.current_deal_data.exchange == "SH":
            commission = Environment.commission_dict[StockType.STOCK_SH.value]
        elif Environment.current_deal_data.exchange == "SZ":
            commission = Environment.commission_dict[StockType.STOCK_SZ.value]

        # 根据经过交易手续费后的成交额，更新成交价格
        if Environment.current_deal_data.offset == Offset.OPEN.value:
            total_commission = commission['open_commission']
            trade_balance *= 1 + total_commission
            Environment.current_deal_data.deal_price = trade_balance / Environment.current_deal_data.deal_volume
            print("commission_calculate")
        elif Environment.current_deal_data.offset == Offset.CLOSE.value:
            total_commission = commission['close_commission'] + commission['tax']
            trade_balance *= 1 - total_commission
            Environment.current_deal_data.deal_price = trade_balance / Environment.current_deal_data.deal_volume
        print(Environment.current_deal_data.deal_price, "wwwwwwwwwwwwwww")

    @classmethod
    def update_position_list(cls, event):
        """
        如果有持仓，更新持仓成本　更新持仓数量
        如果没有吃，增加持仓list
        :param event:
        :return:
        """
        # # 　代码编号相关
        # self.instrument = Empty.EMPTY_STRING.value  # 合约代码
        # self.exchange = Empty.EMPTY_STRING.value  # 交易所代码
        #
        # # 　持仓相关
        # self.average_price = Empty.EMPTY_FLOAT.value  # 持仓均价
        # self.direction = Empty.EMPTY_STRING.value  # 持仓方向
        # self.position = Empty.EMPTY_INT.value  # 持仓数量
        # self.frozen = Empty.EMPTY_INT.value  # 冻结数量
        # self.yesterday_position = Empty.EMPTY_INT.value  # 昨持仓数量
        # self.position_profit = Empty.EMPTY_FLOAT.value  # 持仓盈亏
        Environment.current_position_data.instrument = Environment.current_deal_data.instrument
        Environment.current_position_data.exchange = Environment.current_deal_data.exchange
        Environment.current_position_data.account_id = Environment.current_order_data.session_id
        Environment.current_position_data.frozen += Environment.current_deal_data.deal_volume

        if Environment.bar_position_data_list:
            position_num = 0
            position_hold = False
            for position_data in Environment.bar_position_data_list:
                position_num += 1
                if Environment.current_position_data.instrument == position_data.instrument and \
                        Environment.current_position_data.exchange == position_data.exchange:
                    position_hold = True
                    print(Environment.current_deal_data.offset, "方向"*10)
                    if Environment.current_deal_data.offset == Offset.OPEN.value:
                        total_position = position_data.position + Environment.current_deal_data.deal_volume
                        position_cost_balance = position_data.position * position_data.average_price
                        trade_balance = \
                            Environment.current_deal_data.deal_volume * Environment.current_deal_data.deal_price
                        # 更新持仓成本
                        position_data.average_price = \
                            (position_cost_balance + trade_balance) / total_position
                        # 更新持仓数量
                        position_data.position = total_position
                        # 更新冻结数量
                        position_data.frozen += Environment.current_deal_data.deal_volume
                        print("update_position_list")

                    elif Environment.current_deal_data.offset == Offset.CLOSE.value:
                        total_position = \
                            position_data.position - Environment.current_deal_data.deal_volume
                        position_cost_balance = position_data.position * position_data.average_price
                        trade_balance = \
                            Environment.current_deal_data.deal_volume * Environment.current_deal_data.deal_price
                        if total_position > 0:
                            position_data.average_price = \
                                (position_cost_balance - trade_balance) / total_position
                        else:
                            position_data.average_price = 0
                        position_data.position = total_position
                        print("sell position"*5, position_data.position)

            # 持仓不为空，且不在持仓里面的，append到Environment.bar_position_data_list
            if position_num == len(Environment.bar_position_data_list) and position_hold is False:
                Environment.current_position_data.average_price = Environment.current_deal_data.deal_price
                Environment.current_position_data.position = Environment.current_deal_data.deal_volume
                Environment.bar_position_data_list.append(Environment.current_position_data)



        else:
            Environment.current_position_data.average_price = Environment.current_deal_data.deal_price
            Environment.current_position_data.position = Environment.current_deal_data.deal_volume
            # 持仓为空，append到Environment.bar_position_data_list
            Environment.bar_position_data_list.append(Environment.current_position_data)

        # 更新委托的状态和成交数量，并把此次委托append到Environment.bar_order_data_list
        Environment.current_order_data.status = Status.ALL_TRADED.value
        Environment.current_order_data.deal_volume = Environment.current_deal_data.deal_volume
        Environment.bar_order_data_list.append(Environment.current_order_data)
        # 把此次成交append到Environment.bar_deal_data_list
        Environment.bar_deal_data_list.append(Environment.current_deal_data)




    @classmethod
    def update_account_list(cls, event):
        """
        更新可用资金
        :param event:
        :return:
        """
        if Environment.bar_account_data_list:
            for account in Environment.bar_account_data_list:
                if account.account_id == Environment.current_order_data.session_id:
                    if Environment.current_deal_data.offset == Offset.OPEN.value:
                        # 更新可用资金
                        account.available -= \
                            Environment.current_deal_data.deal_price * Environment.current_deal_data.deal_volume
                    elif Environment.current_deal_data.offset == Offset.CLOSE.value:

                        account.available += \
                            Environment.current_deal_data.deal_price * Environment.current_deal_data.deal_volume

        print("update_account_list")
        pass
