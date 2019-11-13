# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : constant.py.py
# @Project : AmazingQuant

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
    EVENT_BACKTESTING_ANALYSIS = "event_backtesting_analysis"

@unique
class ID(Enum):
    BROKER_ID = "broker"
    FRONT_ID = "front"
    ORDER_ID = "order"
    DEAL_ID = "deal"

class Empty(Enum):
    EMPTY_STRING = ""
    EMPTY_INT = 0
    EMPTY_FLOAT = 0.0

@unique
class RunMode(Enum):
    TRADE = "trade"
    BACKTESTING = "backtesting"

@unique
class Offset(Enum):
    OPEN = "open"
    CLOSE = "close"


@unique
class Status(Enum):
    NOT_REPORTED = "not_reported"
    WITHDRAW = "withdraw"
    NOT_TRADED = "pending"
    PART_TRADED = "partial filled"
    ALL_TRADED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    UNKNOWN = "unknown"

@unique
class PriceType(Enum):
    LIMIT = "limit"
    MARKET = "market"

@unique
class SlippageType(Enum):
    SLIPPAGE_FIX = "slippage_fix"
    SLIPPAGE_PERCENT = "slippage_percent"

@unique
class StockType(Enum):
    STOCK_SH = "stock_SZ"
    STOCK_SZ = "stock_SH"
    STOCK = "stock"

@unique
class RecordDataType(Enum):
    ORDER_DATA = "order_data"
    DEAL_DATA = "deal_data"
    POSITION_DATA = "position_data"
    ACCOUNT_DATA = "account_data"
