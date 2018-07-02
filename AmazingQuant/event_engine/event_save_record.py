# -*- coding: utf-8 -*-

__author__ = "gao"

import copy

from AmazingQuant.environment import Environment
from AmazingQuant.event_engine.event_engine_base import *


class EventSaveRecord(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_SAVE_RECORD.value)

    @classmethod
    def save_current_bar_data(cls, event):
        """
        记录每根bar的资金 持仓 委托　成交
        :param event:
        :return:
        """
        timetag = event.event_data_dict["strategy_data"].timetag
        Environment.order_data_dict[timetag] = Environment.bar_order_data_list
        Environment.deal_data_dict[timetag] = Environment.bar_deal_data_list
        Environment.position_data_dict[timetag] = copy.deepcopy(Environment.bar_position_data_list)
        Environment.account_data_dict[timetag] = copy.deepcopy(Environment.bar_account_data_list)
        # print("记录每根bar的资金 持仓 委托　成交")
