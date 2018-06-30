# -*- coding: utf-8 -*-

__author__ = "gao"

import sys
import os
import time
import copy

import pandas as pd

from AmazingQuant.event_engine.event_engine_base import Event, EventType
from AmazingQuant.environment import Environment
from AmazingQuant.constant import RecordDataType, Period
from AmazingQuant.data_center.get_data import GetData
from AmazingQuant.utils.data_transfer import millisecond_to_date


class EmptyClass(object):
    pass


class EventBacktestingAnalysis(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_BACKTESTING_ANALYSIS.value)

    @classmethod
    def save_backtesting_record_to_csv(cls, event):
        millisecond_timetag = str(int(time.time()) * 1000)
        for data_type in RecordDataType.__members__.values():
            data_type_value = data_type.value
            if data_type_value == RecordDataType.ORDER_DATA.value:
                data_obj = Environment.current_order_data
                data_dict = Environment.order_data_dict

            elif data_type_value == RecordDataType.DEAL_DATA.value:
                data_obj = Environment.current_deal_data
                data_dict = Environment.deal_data_dict

            elif data_type_value == RecordDataType.POSITION_DATA.value:
                data_obj = Environment.current_position_data
                data_dict = Environment.position_data_dict

            elif data_type_value == RecordDataType.ACCOUNT_DATA.value:
                data_obj = Environment.current_account_data
                data_dict = Environment.account_data_dict

            data_property = [i for i in dir(data_obj) if i not in dir(copy.deepcopy(EmptyClass()))]
            print(data_property, dir(copy.deepcopy(EmptyClass)))
            values = []
            for timetag in Environment.benchmark_index:
                timetag_data_list = []
                for current_data in data_dict[timetag]:
                    timetag_data_list.append([current_data.__dict__[property_data] for property_data in data_property])
                print(timetag_data_list)
                timetag_data_df = pd.DataFrame(timetag_data_list, columns=data_property)
                # timetag_data_df.set_index("account_id", inplace=True)
                # print(timetag_data_df)
                values.append(timetag_data_df)
            all_data = pd.concat(values, keys=Environment.benchmark_index)

            # 数据写到缓存
            if data_type_value == RecordDataType.ORDER_DATA.value:
                Environment.backtesting_record_order = all_data

            elif data_type_value == RecordDataType.DEAL_DATA.value:
                Environment.backtesting_record_deal = all_data

            elif data_type_value == RecordDataType.POSITION_DATA.value:
                Environment.backtesting_record_position = all_data

            elif data_type_value == RecordDataType.ACCOUNT_DATA.value:
                Environment.backtesting_record_account = all_data

            all_data.to_csv(
                sys.argv[0][sys.argv[0].rfind(os.sep) + 1:][:-3] + "_" + data_type_value + millisecond_timetag + ".csv")

    @classmethod
    def calculate_backtesting_indicator(cls, event):
        # （１）基准净值
        benchmark_net_asset_value = cls().get_benchmark_net_asset_value(event)
        print(benchmark_net_asset_value, "benchmark_net_asset_value" * 3)

        # （２）策略净值
        strategy_net_asset_value = cls().get_strategy_net_asset_value()
        print(strategy_net_asset_value, "strategy_net_asset_value" * 3)
        # （３）基准年化收益率
        benchmark_year_yield = cls().get_year_yield(benchmark_net_asset_value)
        # （４）策略年化收益率
        strategy_year_yield = cls().get_year_yield(strategy_net_asset_value)
        print(benchmark_year_yield, strategy_year_yield)

        # （５）beta
        
        # （６）alpha
        # （７）volatility
        # （８）sharpe
        # （９）downside_risk
        # （１０）sortino_ratio
        # （１１）tracking_error
        # （１２）information_ratio
        # （１３）max_drawdown



    def get_benchmark_net_asset_value(self, event):
        period = event.event_data_dict["strategy"].period

        data_class = GetData()

        benchmark = event.event_data_dict["strategy"].benchmark

        if period == Period.DAILY.value:
            start_time = millisecond_to_date(millisecond=Environment.benchmark_index[0], format="%Y-%m-%d")
            end_time = millisecond_to_date(millisecond=Environment.benchmark_index[-1], format="%Y-%m-%d")

            benchmark_close = data_class.get_market_data(Environment.daily_data, stock_code=[benchmark],
                                                         field=["close"], start=start_time, end=end_time)
        elif period == Period.ONE_MIN.value:
            start_time = millisecond_to_date(millisecond=Environment.benchmark_index[0], format="%Y-%m-%d %H:%M:%S")
            end_time = millisecond_to_date(millisecond=Environment.benchmark_index[-1], format="%Y-%m-%d %H:%M:%S")

            benchmark_close = data_class.get_market_data(Environment.daily_data, stock_code=[benchmark],
                                                         field=["close"], start=start_time, end=end_time)

        benchmark_close = list(benchmark_close)

        benchmark_net_asset_value = [current_close / benchmark_close[0] for current_close in benchmark_close]

        return benchmark_net_asset_value

    def get_strategy_net_asset_value(self):
        strategy_asset_list = []
        for timetag in Environment.benchmark_index:
            timetag_balance = 0
            for account_data in Environment.account_data_dict[timetag]:
                timetag_balance += account_data.total_balance
            strategy_asset_list.append(timetag_balance)
        strategy_net_asset_value = [timetag_balance / strategy_asset_list[0] for timetag_balance in strategy_asset_list]
        return strategy_net_asset_value

    def get_year_yield(self, net_asset_value):
        year_yield = [100 * (pow(net_asset_value[value], 252.0 / (value + 1)) - 1) for value in
                      range(len(net_asset_value))]
        return year_yield
