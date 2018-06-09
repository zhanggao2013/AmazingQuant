# -*- coding: utf-8 -*-

__author__ = "gao"

from enum import Enum, unique

@unique
class RunMode(Enum):
    BACKTESTING= "backtesting"
    TRADE= "trade"

@unique
class Period(Enum):
    DAILY = "daily"
    ONE_MIN = "1min"

@unique
class RightsAdjustment(Enum):
    NONE = "none"
    FROWARD = "forward"
    BACKWARD = "backward"


@unique
class EventType(Enum):
    EVENT_TIMER = "event_timer"
    EVENT_ORDER = "event_order"
    EVENT_RISK_MANAGEMENT = "event_risk_management"
    EVENT_DEAL = "event_deal"
    EVENT_SAVE_RECORD = "event_save_record"
    EVENT_MARKET = "event_market"
    EVENT_HANDLE_BAR = "event_handle_bar"
    EVENT_LOG = "event_log"
    EVENR_ERROR = "event_error"
