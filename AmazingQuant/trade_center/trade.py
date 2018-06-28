# -*- coding: utf-8 -*-

__author__ = "gao"


from AmazingQuant.constant import *
from AmazingQuant.data_object import OrderData
from AmazingQuant.utils.generate_random_id import generate_random_id
from AmazingQuant.trade_center.event_mission_engine import MissionEngine
from AmazingQuant.environment import Environment
from AmazingQuant.trade_center.event_broker_engine import EventBrokerEngine


class Trade(object):
    def __init__(self, strategy):
        self._strategy = strategy

    def order_lots(self, stock_code="", shares=1, price_type=PriceType.LIMIT, order_price=None,
                   account=""):
        """下单函数"""
        # 代码编号相关
        Environment.current_order_data.order_id = generate_random_id(ID.ORDER_ID.value)
        Environment.current_order_data.instrument = stock_code[:-3]
        Environment.current_order_data.exchange = stock_code[-2:]

        # 　报单相关
        Environment.current_order_data.price_type = price_type
        Environment.current_order_data.order_price = order_price
        if shares > 0:
            Environment.current_order_data.offset = Offset.OPEN.value
        else:
            Environment.current_order_data.offset = Offset.CLOSE.value
            print("shares < 0"*5, Environment.current_order_data.offset)
        Environment.current_order_data.total_volume = abs(shares)
        Environment.current_order_data.deal_volume = 0
        Environment.current_order_data.status = Status.NOT_REPORTED.value



        # CTP相关
        Environment.current_order_data.order_time = self._strategy.timetag
        for account_data in Environment.bar_account_data_list:
            if account_data.account_id[:-9] == account:
                Environment.current_order_data.session_id = account_data.account_id

        MissionEngine().mission_order(strategy=self._strategy)
        if self._strategy.run_mode == RunMode.BACKTESTING.value:
            if Environment.is_send_order:
                EventBrokerEngine().run_broker(strategy=self._strategy)

        elif self._strategy.run_mode == RunMode.TRADE.value:
            """过真实的交易，只做send_order"""
            #send_order()
            pass

    def send_order(self):
        order_data = Environment.current_order_data

        #ctp_send_order(order_data)



if __name__ == "__main__":
    # aa = EventTradeEngine()
    EventTradeEngine().order_lots()
