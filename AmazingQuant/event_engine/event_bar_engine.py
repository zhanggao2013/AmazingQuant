# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_bar_engine.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.strategy_center.event_market import *
from AmazingQuant.strategy_center.event_save_record import *


def run_bar_engine(strategy):
    event_market = EventMarket()
    event_market.event_data_dict["strategy_data"] = strategy
    EventMarket.update_position_frozen(event_market)
    strategy.handle_bar(event_market)
    EventMarket.update_market_data(event_market)
    EventMarket.delete_position_zero(event_market)
    EventMarket.update_position_close(event_market)
    EventMarket.update_account_close(event_market)
    EventMarket.push_new_bar(event_market)

    event_save_record = EventSaveRecord()
    event_save_record.event_data_dict["strategy_data"] = strategy
    EventSaveRecord.save_current_bar_data(event_save_record)

    Environment().refresh_list(event_save_record)

