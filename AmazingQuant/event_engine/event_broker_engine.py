# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import EventType, RunMode
from AmazingQuant.event_engine.event_order import (EventOrder,
                                                   BacktestingOrder)
from AmazingQuant.data_object import OrderData


class EventBrokerEngine(object):

    def broker(self, new_order_data):
        """
        deal 交易撮合，更新　OrderData DealData AccountData PositionData
        OrderData(返回状态：已成　已撤（检查可用资金　可用数量不合格）等)
        :param new_order_data:
        :return:
        """
        ee = EventEngineBase()
        event_order = EventOrder()
        event_order.event_data_dict["data"] = order_data
        ee.put(event_order)
        # ee.register(EventType.EVENT_TIMER.value, simpletest)

        ee.register(EventType.EVENT_ORDER.value, BacktestingOrder.simple_test)

        # ee.registerGeneralHandler(simpletest)
        ee.start(timer=False)
        ee.stop()