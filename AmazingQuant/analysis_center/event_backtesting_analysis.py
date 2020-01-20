# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_backtesting_analysis.py.py
# @Project : AmazingQuant
# ------------------------------

import sys
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
from AmazingQuant.utils.data_transfer import millisecond_to_date
# from pyecharts import Line, Page, Grid


class EmptyClass(object):
    pass


class EventBacktestingAnalysis(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_BACKTESTING_ANALYSIS.value)

    @classmethod
    def save_backtesting_record_to_csv(cls, event):
        millisecond_time_tag = str(int(time.time() * 1000))
        for data_type in RecordDataType.__members__.values():
            data_type_value = data_type.value
            data_obj = None
            data_dict = None
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
            # print(data_property, dir(copy.deepcopy(EmptyClass)))
            values = []
            for time_tag in Environment.benchmark_index:
                time_tag_data_list = []
                for current_data in data_dict[time_tag]:
                    time_tag_data_list.append([current_data.__dict__[property_data] for property_data in data_property])
                # print(time_tag_data_list)
                time_tag_data_df = pd.DataFrame(time_tag_data_list, columns=data_property)
                # time_tag_data_df.set_index('account_id', inplace=True)
                # print(time_tag_data_df)
                values.append(time_tag_data_df)
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
            save_path_dir = event.event_data_dict["strategy_data"].strategy_name
            if not os.path.exists(save_path_dir):
                os.mkdir(save_path_dir)
            all_data.to_csv(save_path_dir + '/' + data_type_value + '.csv')

    @classmethod
    def show_backtesting_indicator(cls, event):
        period = event.event_data_dict['strategy_data'].period
        benchmark = event.event_data_dict['strategy_data'].benchmark
        indicator_dict = {}
        # （１）基准净值
        benchmark_net_asset_value = cls().get_benchmark_net_asset_value(period, benchmark)
        print('benchmark_net_asset_value', benchmark_net_asset_value)

        # （２）策略净值
        strategy_net_asset_value = cls().get_strategy_net_asset_value()
        print('strategy_net_asset_value', strategy_net_asset_value)

        # （３）基准年化收益率
        benchmark_year_yield = cls().get_year_yield(benchmark_net_asset_value)
        print('benchmark_year_yield', benchmark_year_yield)

        # （４）策略年化收益率
        strategy_year_yield = cls().get_year_yield(strategy_net_asset_value)
        print('strategy_year_yield', strategy_year_yield)

        # （５）beta
        beta = cls().get_beta(benchmark_net_asset_value, strategy_net_asset_value)
        print('beta', beta)
        indicator_dict['beta'] = beta

        # （６）alpha
        alpha = cls().get_alpha(benchmark_year_yield, strategy_year_yield, beta)
        print('alpha', alpha)
        indicator_dict['alpha'] = alpha

        # （７）volatility
        volatility = cls().get_volatility(strategy_net_asset_value)
        print('volatility', volatility)
        indicator_dict['volatility'] = volatility

        # （８）sharpe
        sharpe = cls().get_sharp(strategy_year_yield, volatility)
        print('sharpe', sharpe)
        indicator_dict['sharpe'] = sharpe

        # （９）downside_risk
        downside_risk = cls().get_downside_risk(strategy_year_yield)
        print('downside_risk', downside_risk)
        indicator_dict['downside_risk'] = downside_risk

        # （１０）sortino_ratio
        sortino_ratio = cls().get_sortino_ratio(strategy_year_yield, downside_risk)
        print('sortino_ratio', sortino_ratio)
        indicator_dict['sortino_ratio'] = sortino_ratio

        # （１１）tracking_error
        tracking_error = cls().get_tracking_error(benchmark_net_asset_value, strategy_net_asset_value)
        print('tracking_error', tracking_error)
        indicator_dict['tracking_error'] = tracking_error

        # （１２）information_ratio
        information_ratio = cls().get_information_ratio(benchmark_year_yield, strategy_year_yield, tracking_error)
        print('information_ratio', information_ratio)
        indicator_dict['information_ratio'] = information_ratio

        # （１３）max_drawdown
        max_drawdown = cls().get_max_drawdown(strategy_net_asset_value)
        print('max_drawdown', max_drawdown)
        indicator_dict['max_drawdown'] = max_drawdown

        # 展示到html
        period = event.event_data_dict['strategy_data'].period
        if period == Period.DAILY.value:
            time_tag_date = Environment.benchmark_index
        else:
            time_tag_date = [millisecond_to_date(millisecond=i, format='%Y-%m-%d %H:%M:%S') for i in
                            Environment.benchmark_index]

        # page = Page('strategy backtesting indicator')
        # line_net_asset_value = Line('net_asset_value', width=1300, height=400, title_pos='8%')
        # line_net_asset_value.add('benchmark_net_asset_value', time_tag_date,
        #                          [round(i, 4) for i in benchmark_net_asset_value],
        #                          tooltip_tragger='axis', legend_top='3%', is_datazoom_show=True)
        # line_net_asset_value.add('strategy_net_asset_value', time_tag_date,
        #                          [round(i, 4) for i in strategy_net_asset_value],
        #                          tooltip_tragger='axis', legend_top='3%', is_datazoom_show=True)
        # page.add(line_net_asset_value)
        #
        # line_year_yield = Line('year_yield', width=1300, height=400, title_pos='8%')
        # line_year_yield.add('benchmark_year_yield', time_tag_date,
        #                     [round(i, 4) for i in benchmark_year_yield],
        #                     tooltip_tragger='axis', legend_top='3%', is_datazoom_show=True)
        # line_year_yield.add('strategy_year_yield', time_tag_date,
        #                     [round(i, 4) for i in strategy_year_yield],
        #                     tooltip_tragger='axis', legend_top='3%', is_datazoom_show=True)
        # page.add(line_year_yield)
        #
        # for indicator_name, indicator in indicator_dict.items():
        #     cls().add_to_page(page, indicator, indicator_name, time_tag_date)
        #     # print(indicator_name)
        #
        # millisecond_time_tag = str(int(time.time()) * 1000)
        # page.render(path=sys.argv[0][sys.argv[0].rfind(os.sep) + 1:][
        #                  :-3] + '_' + 'strategy backtesting indicator' + millisecond_time_tag + '.html')  # 生成本地 HTML 文件

    # def add_to_page(self, page, indicator, indicator_name, time_tag_date):
    #     line = Line(indicator_name, width=1300, height=400, title_pos='8%')
    #     line.add(indicator_name, time_tag_date, [round(i, 4) for i in indicator],
    #              tooltip_tragger='axis', legend_top='3%', is_datazoom_show=True)
    #     page.add(line)

    def get_benchmark_net_asset_value(self, period, benchmark):
        data_class = GetKlineData()
        benchmark_close = None
        if period == Period.DAILY.value:
            start_time = Environment.benchmark_index[0]
            end_time = Environment.benchmark_index[-1]

            benchmark_close = data_class.get_market_data(Environment.index_daily_data, stock_code=[benchmark],
                                                         field=['close'], start=start_time, end=end_time)
        elif period == Period.ONE_MIN.value:
            start_time = millisecond_to_date(millisecond=Environment.benchmark_index[0], format='%Y-%m-%d %H:%M:%S')
            end_time = millisecond_to_date(millisecond=Environment.benchmark_index[-1], format='%Y-%m-%d %H:%M:%S')
            benchmark_close = data_class.get_market_data(Environment.index_daily_data, stock_code=[benchmark],
                                                         field=['close'], start=start_time, end=end_time)

        benchmark_close = list(benchmark_close)
        benchmark_net_asset_value = [current_close / benchmark_close[0] for current_close in benchmark_close]
        return benchmark_net_asset_value

    def get_strategy_net_asset_value(self):
        strategy_asset_list = []
        for time_tag in Environment.benchmark_index:
            time_tag_balance = 0
            for account_data in Environment.account_data_dict[time_tag]:
                time_tag_balance += account_data.total_balance
            strategy_asset_list.append(time_tag_balance)
        strategy_net_asset_value = [time_tag_balance / strategy_asset_list[0] for time_tag_balance in strategy_asset_list]
        return strategy_net_asset_value

    def get_year_yield(self, net_asset_value):
        # 分钟回测的年化处理，　（计算不对，必须取交易日列表,改变benchmark_time_tag_to_day[value]）
        # benchmark_time_tag_to_day = [int(time_tag - benchmark_index[0]) / 86400000 for time_tag in benchmark_index]
        year_yield = [100 * (pow(net_asset_value[value], 252.0 / value) - 1) if
                      value > 0 else 1 for value in range(len(net_asset_value))]
        return year_yield

    def get_beta(self, benchmark_net_asset_value, strategy_net_asset_value):
        benchmark_net_asset_value_change = np.array([0]) + (
                np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        return np.cov(benchmark_net_asset_value_change, strategy_net_asset_value_change)[0, 1] / np.var(
            benchmark_net_asset_value_change)

    def get_alpha(self, benchmark_year_yield, strategy_year_yield, beta):
        return strategy_year_yield[-1] - (3.0 + beta * (benchmark_year_yield[-1] - 3.0))

    def get_volatility(self, strategy_net_asset_value):
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        return math.sqrt(252) * np.std(strategy_net_asset_value_change)

    def get_sharp(self, strategy_year_yield, volatility):
        return (strategy_year_yield[-1] - 3.0) / volatility

    def get_downside_risk(self, strategy_year_yield):
        downside_strategy_year_yield = [i if i > 3.0 else i == 0 for i in strategy_year_yield]
        return np.std(downside_strategy_year_yield)

    def get_sortino_ratio(self, strategy_year_yield, downside_risk):
        return (strategy_year_yield[-1] - 3.0) / downside_risk

    def get_tracking_error(self, benchmark_net_asset_value, strategy_net_asset_value):
        benchmark_net_asset_value_change = np.array([0]) + (
                np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        benchmark_strategy_diff = benchmark_net_asset_value_change - strategy_net_asset_value_change
        return math.sqrt(252) * np.std(benchmark_strategy_diff)

    def get_information_ratio(self, benchmark_year_yield, strategy_year_yield, tracking_error):
        return (strategy_year_yield[-1] - benchmark_year_yield[-1]) / tracking_error

    def get_max_drawdown(self, strategy_net_asset_value):
        drawdown_list = []
        for time_tag_index in range(len(strategy_net_asset_value)):
            if time_tag_index > 0 and max(strategy_net_asset_value[:time_tag_index]):
                drawdown = 1 - strategy_net_asset_value[time_tag_index] / max(strategy_net_asset_value[:time_tag_index])
            else:
                drawdown = 0
            drawdown_list.append(drawdown)

        max_drawdown_list = []
        for time_tag_index in range(len(drawdown_list)):
            if time_tag_index > 0:
                max_drawdown = 100 * max(drawdown_list[:time_tag_index + 1])
            else:
                max_drawdown = 0
            max_drawdown_list.append(max_drawdown)

        return max_drawdown_list
