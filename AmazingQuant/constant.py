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
class DatabaseName(Enum):
    MARKET_DATA_DAILY = "market_data_daily"
    FINANCIAL_DATA = "financial_data"
    MARKET_DATA_ONE_MIN = "market_data_1min"


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

@unique
class ID(Enum):
    BROKER_ID = "broker"
    FRONT_ID = "front"
    SESSION_ID = "session"
    ACCOUNT_ID = "account"
    ORDER_ID = "order"
    DEAL_ID = "deal"


@unique
class Empty(Enum):
    EMPTY_STRING = ""
    EMPTY_INT = 0
    EMPTY_FLOAT = 0.0