# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_market import *
from AmazingQuant.event_engine.event_save_record import *


def initialize_current_bar_data(timetag):
    Environment.order_data_dict[timetag] = []
    Environment.deal_data_dict[timetag] = []
    Environment.position_data_dict[timetag] = []
    Environment.account_data_dict[timetag] = []


def run_bar_engine(strategy):
    """

    """
    bar_engine = EventEngineBase()
    event_market = EventMarket()
    event_market.event_data_dict["strategy_data"] = strategy

    bar_engine.put(event_market)
    bar_engine.register(EventType.EVENT_MARKET.value, EventMarket.update_position_frozen)
    bar_engine.register(EventType.EVENT_MARKET.value, strategy.handle_bar)
    bar_engine.register(EventType.EVENT_MARKET.value, EventMarket.push_new_bar)

    bar_engine.register(EventType.EVENT_MARKET.value, EventMarket.delete_position_zero)
    bar_engine.register(EventType.EVENT_MARKET.value, EventMarket.update_position_close)
    bar_engine.register(EventType.EVENT_MARKET.value, EventMarket.update_account_close)

    event_save_record = EventSaveRecord()
    event_save_record.event_data_dict["strategy_data"] = strategy
    bar_engine.put(event_save_record)
    bar_engine.register(EventType.EVENT_SAVE_RECORD.value, EventSaveRecord.save_current_bar_data)
    bar_engine.register(EventType.EVENT_SAVE_RECORD.value, Environment().refresh_list)

    bar_engine.start(timer=True)
    bar_engine.stop()

