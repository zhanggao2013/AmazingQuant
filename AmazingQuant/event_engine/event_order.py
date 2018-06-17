# -*- coding: utf-8 -*-

__author__ = "gao"

from datetime import datetime

from AmazingQuant.event_engine.event_engine_base import EventEngineBase, Event
from AmazingQuant.constant import EventType, ID
from AmazingQuant.environment import Environment

class EventOrder(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_ORDER.value)


class BacktestingOrder(object):
    def simple_test(event=EventOrder()):
        print('处理每秒触发的计时器事件：{}'.format(str(datetime.now())))
        Environment.account[ID.ACCOUNT_ID] = 1




