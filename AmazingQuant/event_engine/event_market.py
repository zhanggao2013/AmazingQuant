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
    def push_new_bar(cls, event):
        event.event_data_dict["strategy_data"].bar_index += 1

    @classmethod
    def update_position_close(cls, event):
        """
        更新bar_close持仓盈亏　和　今仓冻结数量
        :param event:
        :return:
        """
        current_timetag = event.event_data_dict["strategy_data"].timetag
        current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
        data_class = GetData()

        current_day = millisecond_to_date(event.event_data_dict["strategy_data"].timetag, "%d")
        if event.event_data_dict["strategy_data"].bar_index > 0:
            last_timetag = Environment.benchmark_index[event.event_data_dict["strategy_data"].bar_index-1]
            last_day = millisecond_to_date(last_timetag, "%d")

        if Environment.bar_position_data_list:
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                 field=["close"],
                                                                 start='%Y%m%d',
                                                                 end=current_date)
                position_data.position_profit = position_data.position * (
                        current_close_price - position_data.average_price)

                if event.event_data_dict["strategy_data"].bar_index > 0 and last_day != current_day:
                    position_data.frozen = 0
        print("更新bar_close持仓盈亏　和　今仓冻结数量")

    @classmethod
    def update_account_close(cls, event):
        """
        用bar_close更新总资产
        :param event:
        :return:
        """
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
        Environment.current_account_data.balance = Environment.current_account_data.available + hold_balance
        print("更新bar_close总资产")