# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import EventType, RunMode
from AmazingQuant.event_engine.event_order import (EventOrder,
                                                   BacktestingOrder)
from AmazingQuant.data_object import OrderData


class EventTradeEngine(object):
    def __init__(self, run_mode):
        self._run_mode = run_mode

    def order_lots(self, offset="buy", shares=1, style="fix", order_price=None,
                   account_id=""):
        """测试函数"""
        order_data = OrderData()
        order_data.account_id = account_id

        ee = EventEngineBase()
        event_order = EventOrder()
        event_order.event_data_dict["data"] = order_data
        ee.put(event_order)
        # ee.register(EventType.EVENT_TIMER.value, simpletest)
        if self._run_mode == RunMode.BACKTESTING.value:
            ee.register(EventType.EVENT_ORDER.value, BacktestingOrder.simple_test)
        elif self._run_mode == RunMode.TRADE.value:
            pass
        # ee.registerGeneralHandler(simpletest)
        ee.start(timer=False)
        ee.stop()


if __name__ == "__main__":
    # aa = EventTradeEngine()
    EventTradeEngine().order_lots()
