# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_market.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.environment import Environment
from AmazingQuant.event_engine.event_engine_base import *
from AmazingQuant.data_center.get_data.get_kline import GetKlineData


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
                current_day = event.event_data_dict["strategy_data"].time_tag
                last_day = Environment.benchmark_index[event.event_data_dict["strategy_data"].bar_index - 1]
                for position_data in Environment.bar_position_data_list:
                    if last_day != current_day:
                        position_data.frozen = 0
                        # print("更新今仓冻结数量")
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
        # print("delete_position_zero" )
        # print(len(Environment.bar_position_data_list))

        Environment.bar_position_data_list = [position_data for position_data in Environment.bar_position_data_list if
                                              position_data.position != 0]

        # print(len(Environment.bar_position_data_list))
        pass

    @classmethod
    def update_position_close(cls, event):
        """
        更新bar_close持仓盈亏
        :param event:
        :return:
        """
        if Environment.bar_position_data_list:
            current_date = event.event_data_dict["strategy_data"].time_tag
            data_class = GetKlineData()
            for position_data in Environment.bar_position_data_list:
                stock_code = position_data.instrument + "." + position_data.exchange
                current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                 field=["close"],
                                                                 start=current_date,
                                                                 end=current_date)
                position_data.position_profit = position_data.position * (
                        current_close_price - position_data.average_price)
        # print("更新bar_close持仓盈亏")

    @classmethod
    def update_account_close(cls, event):
        """
        用bar_close更新总资产
        :param event:
        :return:
        """
        current_date = event.event_data_dict["strategy_data"].time_tag
        data_class = GetKlineData()

        if Environment.bar_position_data_list:
            for account in Environment.bar_account_data_list:
                # 分资金账号update
                hold_balance = 0
                for position_data in Environment.bar_position_data_list:
                    if account.account_id == position_data.account_id:
                        stock_code = position_data.instrument + "." + position_data.exchange
                        current_close_price = data_class.get_market_data(Environment.daily_data, stock_code=[stock_code],
                                                                         field=["close"],
                                                                         start=current_date,
                                                                         end=current_date)
                        hold_balance += position_data.position * current_close_price
                    account.total_balance = account.available + hold_balance
        # print("更新bar_close总资产test0"*5,Environment.bar_account_data_list[0].total_balance)
        # print("更新bar_close总资产test1" * 5, Environment.bar_account_data_list[1].total_balance)
