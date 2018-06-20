# -*- coding: utf-8 -*-

__author__ = "gao"


from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.event_engine.event_order import *

class MissionEngine(object):

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
        # new_order_data = order_data
        # return new_order_data
        pass