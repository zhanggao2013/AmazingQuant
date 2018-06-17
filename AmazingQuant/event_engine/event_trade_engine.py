# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import EventType
from AmazingQuant.event_engine.event_order import (EventOrder,
                                                   simple_test)


class EventTradeEngine(object):
    def order_lots(self):
        """测试函数"""

        ee = EventEngineBase()
        event_order = EventOrder()
        ee.put(event_order)
        # ee.register(EventType.EVENT_TIMER.value, simpletest)
        ee.register(EventType.EVENT_ORDER.value, simple_test)
        # ee.registerGeneralHandler(simpletest)
        ee.start(timer=False)
        ee.stop()


if __name__ == "__main__":
    #aa = EventTradeEngine()
    EventTradeEngine().order_lots()
