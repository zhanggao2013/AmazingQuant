# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import EventType, RunMode
from AmazingQuant.event_engine.event_order import (EventOrder,
                                                   BacktestingOrder)
from AmazingQuant.data_object import OrderData
from AmazingQuant.event_engine.event_broker_engine import EventBrokerEngine

class EventTradeEngine(object):
    def __init__(self, run_mode):
        self._run_mode = run_mode

    def order_lots(self, offset="buy", shares=1, style="fix", order_price=None,
                   account_id=""):
        """下单函数"""
        order_data = OrderData()
        order_data.account_id = account_id
        new_order_data = self.run_order(order_data)

        if self._run_mode == RunMode.BACKTESTING.value:
            send_order(new_order_data)
            EventBrokerEngine.broker()
        elif self._run_mode == RunMode.TRADE.value:
            """过真实的send，只做send_order"""
            send_order(new_order_data)
            pass


    def run_order(self, order_data):
        """
        order  和　risk management 两个事件, ,同样使用event_engine,本地计算的engine
        在risk management
        更新　OrderData,的状态：已报
        :param order_data:
        :return:
        """

        return new_order_data
        pass






if __name__ == "__main__":
    # aa = EventTradeEngine()
    EventTradeEngine().order_lots()
