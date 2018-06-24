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
                   account_id=""):
        """下单函数"""
        order_data = OrderData()
        # 代码编号相关
        order_data.order_id = generate_random_id(ID.ORDER_ID.value)
        order_data.instrument = stock_code[:-2]
        order_data.exchange = stock_code[-2:]

        # 　报单相关
        order_data.price_type = price_type
        order_data.order_price = order_price
        if shares > 0:
            order_data.offset = Offset.OPEN.value
        else:
            order_data.offset = Offset.CLOSE.value
        order_data.total_volume = shares
        order_data.deal_volume = 0
        order_data.status = Status.NOT_REPORTED.value

        # CTP相关
        order_data.order_time = self._strategy.timetag
        order_data.session_id = generate_random_id(account_id)

        Environment.current_order_data = order_data
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
