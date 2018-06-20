# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.environment import Environment
from AmazingQuant.event_engine.event_engine_base import *
from AmazingQuant.data_center.get_data import GetData
from AmazingQuant.utils.data_transfer import *


class EventMarket(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_MARKET.value)

    @classmethod
    def update_position_open(cls, event):
        current_timetag = event.event_data_dict["strategy_data"].timetag
        current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
        data_class = GetData()

        if Environment.bar_position_data_list:
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_open_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                field=["open"],
                                                                start='%Y%m%d',
                                                                end=current_date)
                position_data.position_profit = position_data.position * (
                        current_open_price - position_data.average_price)
        print("更新bar_open持仓盈亏")

    @classmethod
    def update_account_open(cls, event):
        current_timetag = event.event_data_dict["strategy_data"].timetag
        current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
        data_class = GetData()

        hold_balance = 0
        if Environment.bar_position_data_list:
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_open_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                field=["open"],
                                                                start='%Y%m%d',
                                                                end=current_date)
                hold_balance += position_data.position * current_open_price
        Environment.current_account_data.balance = Environment.current_account_data.avaliable + hold_balance
        print("更新bar_open总资产")

    @classmethod
    def push_new_bar(cls, event):
        event.event_data_dict["strategy_data"].bar_index += 1

    @classmethod
    def update_position_close(cls, event):
        current_timetag = event.event_data_dict["strategy_data"].timetag
        current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
        data_class = GetData()

        if Environment.bar_position_data_list:
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                 field=["close"],
                                                                 start='%Y%m%d',
                                                                 end=current_date)
                position_data.position_profit = position_data.position * (
                        current_close_price - position_data.average_price)
        print("更新bar_close持仓盈亏")

    @classmethod
    def update_account_close(cls, event):
        current_timetag = event.event_data_dict["strategy_data"].timetag
        current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
        data_class = GetData()

        hold_balance = 0
        if Environment.bar_position_data_list:
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                 field=["close"],
                                                                 start='%Y%m%d',
                                                                 end=current_date)
                hold_balance += position_data.position * current_close_price
        Environment.current_account_data.balance = Environment.current_account_data.avaliable + hold_balance
        print("更新bar_close总资产")
