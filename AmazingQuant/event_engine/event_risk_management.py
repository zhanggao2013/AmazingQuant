# -*- coding: utf-8 -*-

__author__ = "gao"

from datetime import datetime

from AmazingQuant.event_engine.event_engine_base import EventEngineBase, Event
from AmazingQuant.constant import EventType, ID
from AmazingQuant.environment import Environment


class EventRiskManagement(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_RISK_MANAGEMENT.value)

    @classmethod
    def black_namelist_check(cls, event):
        pass