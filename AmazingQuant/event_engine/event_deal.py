# -*- coding: utf-8 -*-

__author__ = "gao"


from AmazingQuant.event_engine.event_engine_base import Event
from AmazingQuant.environment import Environment
from AmazingQuant.data_center.get_data import GetData
from AmazingQuant.constant import *


class EventDeal(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_DEAL.value)

    @classmethod
    def deal_price_calculate(cls, event):
        event.event_data_dict["strategy"].
        print("qwe")