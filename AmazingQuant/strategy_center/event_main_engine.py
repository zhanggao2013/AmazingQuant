# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.environment import Environment


def initialize_current_bar_data(timetag):
    Environment.order_data_dict[timetag] = []
    Environment.deal_data_dict[timetag] = []
    Environment.position_data_dict[timetag] = []
    Environment.account_data_dict[timetag] = []


def update_current_bar_data(timetag):
    Environment.order_data_dict[timetag] = Environment.bar_order_data_list
    Environment.deal_data_dict[timetag] = Environment.bar_deal_data_list
    Environment.position_data_dict[timetag] = Environment.bar_position_data_list
    Environment.account_data_dict[timetag] = Environment.bar_account_data_list
