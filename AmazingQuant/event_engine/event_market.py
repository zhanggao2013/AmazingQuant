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
    def update_position_frozen(cls, event):
        """
        每根bar运行前，更新今日持仓冻结数量
        :param event:
        :return:
        """
        if event.event_data_dict["strategy_data"].bar_index > 0:
            if Environment.bar_position_data_list:
                current_day = millisecond_to_date(event.event_data_dict["strategy_data"].timetag, "%d")
                last_timetag = Environment.benchmark_index[event.event_data_dict["strategy_data"].bar_index - 1]
                last_day = millisecond_to_date(last_timetag, "%d")
                for position_data in Environment.bar_position_data_list:
                    if last_day != current_day:
                        position_data.frozen = 0
                        print("更新今仓冻结数量")
        pass

    @classmethod
    def push_new_bar(cls, event):
        event.event_data_dict["strategy_data"].bar_index += 1

    @classmethod
    def delete_position_zero(cls, event):
        """
        删除持仓数量为０的position
        :param event:
        :return:
        """
        if Environment.bar_position_data_list:
            for position_num in range(len(Environment.bar_position_data_list)):
                if Environment.bar_position_data_list[position_num] == 0:
                    del Environment.bar_position_data_list[position_num]

        pass

    @classmethod
    def update_position_close(cls, event):
        """
        更新bar_close持仓盈亏
        :param event:
        :return:
        """
        if Environment.bar_position_data_list:
            current_timetag = event.event_data_dict["strategy_data"].timetag
            current_date = millisecond_to_date(current_timetag, format='%Y-%m-%d')
            data_class = GetData()
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                 field=["close"],
                                                                 start=current_date,
                                                                 end=current_date)
                position_data.position_profit = position_data.position * (
                        current_close_price - position_data.average_price)
        print("更新bar_close持仓盈亏")

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
                                                                 start=current_date,
                                                                 end=current_date)
                hold_balance += position_data.position * current_close_price
        Environment.current_account_data.balance = Environment.current_account_data.available + hold_balance
        print("更新bar_close总资产")


