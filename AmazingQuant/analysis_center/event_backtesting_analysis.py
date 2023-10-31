# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_backtesting_analysis.py.py
# @Project : AmazingQuant
# ------------------------------

import json
import os
import time
import copy
import math

import pandas as pd
import numpy as np

from AmazingQuant.event_engine.event_engine_base import Event, EventType
from AmazingQuant.environment import Environment
from AmazingQuant.constant import RecordDataType, Period
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.analysis_center.position_analysis import PositionAnalysis
from AmazingQuant.analysis_center.net_value_analysis import NetValueAnalysis
from AmazingQuant.data_object import AccountData, OrderData, DealData, PositionData
from AmazingQuant.analysis_center.show_result import ShowResult


# from pyecharts import Line, Page, Grid


class EmptyClass(object):
    pass


class EventBacktestingAnalysis(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_BACKTESTING_ANALYSIS.value)

    @classmethod
    def save_backtesting_record_to_csv(cls, event):
        for data_type in RecordDataType.__members__.values():
            data_type_value = data_type.value
            data_obj = None
            data_dict = None
            data_property = []
            if data_type_value == RecordDataType.ORDER_DATA.value:
                data_dict = Environment.order_data_dict
                data_property = list(json.loads(OrderData().__str__()).keys())

            elif data_type_value == RecordDataType.DEAL_DATA.value:
                data_dict = Environment.deal_data_dict
                data_property = list(json.loads(DealData().__str__()).keys())

            elif data_type_value == RecordDataType.POSITION_DATA.value:
                data_dict = Environment.position_data_dict
                data_property = list(json.loads(PositionData().__str__()).keys())

            elif data_type_value == RecordDataType.ACCOUNT_DATA.value:
                data_dict = Environment.account_data_dict
                data_property = list(json.loads(AccountData().__str__()).keys())

            values = []
            for time_tag in Environment.benchmark_index:
                time_tag_data_list = []
                for current_data in data_dict[time_tag]:
                    time_tag_data_list.append([current_data.__dict__[property_data] for property_data in data_property])
                # Environment.logger.info(time_tag_data_list)
                time_tag_data_df = pd.DataFrame(time_tag_data_list, columns=data_property)
                time_tag_data_df.set_index('account_id', inplace=True)
                # Environment.logger.info(time_tag_data_df)
                values.append(time_tag_data_df)
            all_data = pd.concat(values, keys=Environment.benchmark_index, names=('time_tag', 'account_id'))

            # 数据写到缓存
            if data_type_value == RecordDataType.ORDER_DATA.value:
                Environment.backtesting_record_order = all_data

            elif data_type_value == RecordDataType.DEAL_DATA.value:
                Environment.backtesting_record_deal = all_data

            elif data_type_value == RecordDataType.POSITION_DATA.value:
                Environment.backtesting_record_position = all_data

            elif data_type_value == RecordDataType.ACCOUNT_DATA.value:
                Environment.backtesting_record_account = all_data
            save_path_dir = event.event_data_dict["strategy_data"].strategy_name
            if not os.path.exists(save_path_dir):
                os.mkdir(save_path_dir)
            all_data.to_csv(save_path_dir + '/' + data_type_value + '.csv')

    @classmethod
    def show_backtesting_indicator(cls, event):
        benchmark = event.event_data_dict['strategy_data'].benchmark
        account = event.event_data_dict['strategy_data'].account
        data_class = GetKlineData()
        start_time = Environment.benchmark_index[0]
        end_time = Environment.benchmark_index[-1]

        account_df = Environment.backtesting_record_account
        benchmark_df = data_class.get_market_data(Environment.index_daily_data, stock_code=[benchmark],
                                                  field=['close'], ).to_frame(name='close')
        account_df = account_df[account_df.index.get_level_values(1) == account[0]]
        account_df.reset_index(level='account_id', drop=True, inplace=True)
        net_value_analysis_obj = NetValueAnalysis(account_df, benchmark_df, start_time, end_time)

        net_analysis_result = net_value_analysis_obj.cal_net_analysis_result()
        for i in net_analysis_result:
            Environment.logger.info(i, net_analysis_result[i])

        # 持仓数据转pandas
        position_data_df = Environment.backtesting_record_position

        position_data_df = position_data_df[position_data_df.index.get_level_values(1) == account[0]]
        position_analysis_obj = PositionAnalysis(position_data_df)
        position_analysis_result = position_analysis_obj.cal_position_analysis_result()
        for i in position_analysis_result:
            Environment.logger.info(i, position_analysis_result[i])

        show_result_object = ShowResult(net_analysis_result, position_analysis_result)
        save_path_dir = event.event_data_dict["strategy_data"].strategy_name + '/'
        if not os.path.exists(save_path_dir):
            os.mkdir(save_path_dir)
        show_result_object.show_page(save_path_dir)

