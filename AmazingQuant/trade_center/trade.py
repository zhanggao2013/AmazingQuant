# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import *
from AmazingQuant.event_engine.event_order import *
from AmazingQuant.data_object import OrderData
from AmazingQuant.trade_center.event_broker_engine import EventBrokerEngine
from AmazingQuant.utils.generate_random_id import generate_random_id


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
        order_data.status = Status.NOTTRADED.value

        # CTP相关
        order_data.order_time = self._strategy.timetag
        order_data.session_id = generate_random_id(account_id)

        Environment.current_order_data = order_data
        new_order_data = self.mission_order()

        '''if self._strategy.run_mode == RunMode.BACKTESTING.value:
            self.send_order(new_order_data)
            # EventBrokerEngine.broker()
            pass
        elif self._strategy.run_mode == RunMode.TRADE.value:
            """过真实的send，只做send_order"""
            # send_order(new_order_data)
            pass'''

    def send_order(self, order_data):
        pass

    def mission_order(self):
        """
        order  和　risk management 两个事件, ,同样使用event_engine,本地计算的engine,重新隔离出一个engine
        在risk management
        更新　OrderData,的状态：已报
        :param order_data:
        :return:
        """
        mission_engine = EventEngineBase()
        event_order = EventOrder()
        event_order.event_data_dict["data"] = Environment.current_order_data

        mission_engine.put(event_order)

        mission_engine.register(EventType.EVENT_ORDER.value, EventOrder.integer_conversion)

        mission_engine.start(timer=False)
        mission_engine.stop()
        #new_order_data = order_data
        #return new_order_data
        pass


if __name__ == "__main__":
    # aa = EventTradeEngine()
    EventTradeEngine().order_lots()
