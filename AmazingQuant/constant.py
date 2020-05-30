# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : constant.py.py
# @Project : AmazingQuant
# ------------------------------

from enum import Enum, unique


@unique
class RunMode(Enum):
    BACKTESTING = 'backtesting'
    TRADE = 'trade'


@unique
class Period(Enum):
    DAILY = 'daily'
    ONE_MIN = '1min'


@unique
class RightsAdjustment(Enum):
    NONE = 'none'
    FROWARD = 'forward'
    BACKWARD = 'backward'
    GEOMETRIC_FROWARD = 'geometric_forward'
    GEOMETRIC_BACKWARD = 'geometric_backward'


@unique
class AdjustmentFactor(Enum):
    BACKWARD_ADJ_FACTOR = 'backward_adj_factor'
    FROWARD_ADJ_FACTOR = 'forward_adj_factor'
    GEOMETRIC_BACKWARD_ADJ_FACTOR = 'geometric_backward_adj_factor'
    GEOMETRIC_FROWARD_ADJ_FACTOR = 'geometric_forward_adj_factor'


@unique
class DatabaseName(Enum):
    A_SHARE_KLINE_DAILY = 'a_share_kline_daily'
    STOCK_BASE_DATA = 'stock_base_data'
    INDICATOR = 'indicator'
    INDEX_KLINE_DAILY = 'index_kline_daily'
    MARKET_DATA_ONE_MIN = 'market_data_1min'


@unique
class LocalDataFolderName(Enum):
    CALENDAR = 'calendar'

    INDEX_MEMBER = 'index_member'

    ADJ_FACTOR = 'adj_factor'

    MARKET_DATA = 'market_data'
    KLINE_DAILY = 'kline_daily'
    A_SHARE = 'a_share'
    INDEX = 'index'

    SWS_INDEX = 'sws_index'

    INDUSTRY_CLASS = 'industry_class'

    INDICATOR_EVERYDAY = 'indicator_everyday'

    FACTOR = 'factor'




@unique
class EventType(Enum):
    EVENT_TIMER = 'event_timer'
    EVENT_ORDER = 'event_order'
    EVENT_RISK_MANAGEMENT = 'event_risk_management'
    EVENT_DEAL = 'event_deal'
    EVENT_SAVE_RECORD = 'event_save_record'
    EVENT_MARKET = 'event_market'
    EVENT_HANDLE_BAR = 'event_handle_bar'
    EVENT_LOG = 'event_log'
    EVENR_ERROR = 'event_error'
    EVENT_BACKTESTING_ANALYSIS = 'event_backtesting_analysis'


@unique
class ID(Enum):
    BROKER_ID = 'broker'
    FRONT_ID = 'front'
    ORDER_ID = 'order'
    DEAL_ID = 'deal'


class Empty(Enum):
    EMPTY_STRING = ''
    EMPTY_INT = 0
    EMPTY_FLOAT = 0.0


@unique
class RunMode(Enum):
    TRADE = 'trade'
    BACKTESTING = 'backtesting'


@unique
class Offset(Enum):
    OPEN = 'open'
    CLOSE = 'close'


@unique
class Status(Enum):
    NOT_REPORTED = 'not_reported'
    WITHDRAW = 'withdraw'
    NOT_TRADED = 'pending'
    PART_TRADED = 'partial filled'
    ALL_TRADED = 'filled'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'
    UNKNOWN = 'unknown'


@unique
class PriceType(Enum):
    LIMIT = 'limit'
    MARKET = 'market'


@unique
class SlippageType(Enum):
    SLIPPAGE_FIX = 'slippage_fix'
    SLIPPAGE_PERCENT = 'slippage_percent'


@unique
class StockType(Enum):
    STOCK_SH = 'stock_SZ'
    STOCK_SZ = 'stock_SH'
    STOCK = 'stock'


@unique
class RecordDataType(Enum):
    ORDER_DATA = 'order_data'
    DEAL_DATA = 'deal_data'
    POSITION_DATA = 'position_data'
    ACCOUNT_DATA = 'account_data'
