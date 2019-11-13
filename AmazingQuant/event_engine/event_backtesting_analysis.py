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
import collections

import pandas as pd
import numpy as np

from AmazingQuant.event_engine.event_engine_base import Event, EventType
from AmazingQuant.environment import Environment
from AmazingQuant.constant import RecordDataType, Period
from AmazingQuant.data_center.get_data import GetData
from AmazingQuant.utils.data_transfer import millisecond_to_date
from pyecharts import Line, Page, Grid


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
            # print(data_property, dir(copy.deepcopy(EmptyClass)))
            values = []
            for timetag in Environment.benchmark_index:
                timetag_data_list = []
                for current_data in data_dict[timetag]:
                    timetag_data_list.append([current_data.__dict__[property_data] for property_data in data_property])
                # print(timetag_data_list)
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
    def show_backtesting_indicator(cls, event):
        indicator_dict = {}
        indicator_dict = collections.OrderedDict()
        # （１）基准净值
        benchmark_net_asset_value = cls().get_benchmark_net_asset_value(event)
        # print(benchmark_net_asset_value, "benchmark_net_asset_value" * 3)

        # （２）策略净值
        strategy_net_asset_value = cls().get_strategy_net_asset_value()
        # print(strategy_net_asset_value, "strategy_net_asset_value")

        # （３）基准年化收益率
        benchmark_year_yield = cls().get_year_yield(benchmark_net_asset_value)

        # （４）策略年化收益率
        strategy_year_yield = cls().get_year_yield(strategy_net_asset_value)
        # print(benchmark_year_yield, strategy_year_yield)

        # （５）beta
        beta = cls().get_beta(benchmark_net_asset_value, strategy_net_asset_value)
        # print(beta)
        indicator_dict["beta"] = beta

        # （６）alpha
        alpha = cls().get_alpha(benchmark_year_yield, strategy_year_yield, beta)
        # print(alpha)
        indicator_dict["alpha"] = alpha

        # （７）volatility
        volatility = cls().get_volatility(strategy_net_asset_value)
        # print(volatility)
        indicator_dict["volatility"] = volatility

        # （８）sharpe
        sharpe = cls().get_sharp(strategy_year_yield, volatility)
        # print(sharpe)
        indicator_dict["sharpe"] = sharpe

        # （９）downside_risk
        downside_risk = cls().get_downside_risk(strategy_year_yield)
        # print(downside_risk)
        indicator_dict["downside_risk"] = downside_risk

        # （１０）sortino_ratio
        sortino_ratio = cls().get_sortino_ratio(strategy_year_yield, downside_risk)
        # print(sortino_ratio)
        indicator_dict["sortino_ratio"] = sortino_ratio

        # （１１）tracking_error
        tracking_error = cls().get_tracking_error(benchmark_net_asset_value, strategy_net_asset_value)
        # print(tracking_error)
        indicator_dict["tracking_error"] = tracking_error

        # （１２）information_ratio
        information_ratio = cls().get_information_ratio(benchmark_year_yield, strategy_year_yield, tracking_error)
        # print(information_ratio)
        indicator_dict["information_ratio"] = information_ratio

        # （１３）max_drawdown
        max_drawdown = cls().get_max_drawdown(strategy_net_asset_value)
        # print(max_drawdown)
        indicator_dict["max_drawdown"] = max_drawdown

        # 展示到html
        period = event.event_data_dict["strategy"].period
        if period == Period.DAILY.value:
            timetag_date = [millisecond_to_date(millisecond=i, format="%Y-%m-%d") for i in Environment.benchmark_index]
        else:
            timetag_date = [millisecond_to_date(millisecond=i, format="%Y-%m-%d %H:%M:%S") for i in
                            Environment.benchmark_index]

        page = Page("strategy backtesting indicator")
        line_net_asset_value = Line("net_asset_value", width=1300, height=400, title_pos="8%")
        line_net_asset_value.add("benchmark_net_asset_value", timetag_date,
                                 [round(i, 4) for i in benchmark_net_asset_value],
                                 tooltip_tragger="axis", legend_top="3%", is_datazoom_show=True)
        line_net_asset_value.add("strategy_net_asset_value", timetag_date,
                                 [round(i, 4) for i in strategy_net_asset_value],
                                 tooltip_tragger="axis", legend_top="3%", is_datazoom_show=True)
        page.add(line_net_asset_value)

        line_year_yield = Line("year_yield", width=1300, height=400, title_pos="8%")
        line_year_yield.add("benchmark_year_yield", timetag_date,
                            [round(i, 4) for i in benchmark_year_yield],
                            tooltip_tragger="axis", legend_top="3%", is_datazoom_show=True)
        line_year_yield.add("strategy_year_yield", timetag_date,
                            [round(i, 4) for i in strategy_year_yield],
                            tooltip_tragger="axis", legend_top="3%", is_datazoom_show=True)
        page.add(line_year_yield)

        for indicator_name, indicator in indicator_dict.items():
            cls().add_to_page(page, indicator, indicator_name, timetag_date)
            # print(indicator_name)

        millisecond_timetag = str(int(time.time()) * 1000)
        page.render(path=sys.argv[0][sys.argv[0].rfind(os.sep) + 1:][
                         :-3] + "_" + "strategy backtesting indicator" + millisecond_timetag + ".html")  # 生成本地 HTML 文件

    def add_to_page(self, page, indicator, indicator_name, timetag_date):
        line = Line(indicator_name, width=1300, height=400, title_pos="8%")
        line.add(indicator_name, timetag_date, [round(i, 4) for i in indicator],
                 tooltip_tragger="axis", legend_top="3%", is_datazoom_show=True)
        page.add(line)

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
        # 分钟回测的年化处理，　（计算不对，必须取交易日列表,改变benchmark_timetag_to_day[value]）
        benchmark_index = Environment.benchmark_index
        benchmark_timetag_to_day = [int(timetag - benchmark_index[0]) / 86400000 for timetag in benchmark_index]
        year_yield = [100 * (pow(net_asset_value[value], 252.0 / benchmark_timetag_to_day[value]) - 1) if
                      benchmark_timetag_to_day[value] > 0 else 1 for value in
                      range(len(net_asset_value))]

        return year_yield

    def get_beta(self, benchmark_net_asset_value, strategy_net_asset_value):
        benchmark_net_asset_value_change = np.array([0]) + (
                np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        beta_list = []
        for timetag_index in range(len(Environment.benchmark_index)):
            benchmark_net_asset_value_timetag = benchmark_net_asset_value_change[:timetag_index + 1]
            strategy_net_asset_value_timetag = strategy_net_asset_value_change[:timetag_index + 1]
            if len(benchmark_net_asset_value_timetag) > 1:
                beta = (np.cov(benchmark_net_asset_value_timetag, strategy_net_asset_value_timetag)[0, 1]) / np.var(
                    benchmark_net_asset_value_timetag)
            else:
                beta = 0
            beta_list.append(beta)
        return beta_list

    def get_alpha(self, benchmark_year_yield, strategy_year_yield, beta):
        alpha_list = []
        for i in range(len(benchmark_year_yield)):
            alpha = strategy_year_yield[i] - (3.0 + beta[i] * (benchmark_year_yield[i] - 3.0))
            alpha_list.append(alpha)
        return alpha_list

    def get_volatility(self, strategy_net_asset_value):
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        volatility_list = []
        for timetag_index in range(len(strategy_net_asset_value)):
            if timetag_index > 0:
                volatility = math.sqrt(252) * np.std(strategy_net_asset_value_change[:timetag_index + 1])
            else:
                volatility = 0
            volatility_list.append(volatility)
        return volatility_list

    def get_sharp(self, strategy_year_yield, volatility):
        sharp_list = []
        for timetag_index in range(len(strategy_year_yield)):
            if volatility[timetag_index] > 0:
                sharp = (strategy_year_yield[timetag_index] - 3.0) / volatility[timetag_index]
            else:
                sharp = 0
            sharp_list.append(sharp)
        return sharp_list

    def get_downside_risk(self, strategy_year_yield):
        downside_strategy_year_yield = [i if i > 3.0 else i == 0 for i in strategy_year_yield]
        downside_risk_list = []
        for timetag_index in range(len(downside_strategy_year_yield)):
            if timetag_index > 0:
                downside_risk = np.std(downside_strategy_year_yield[:timetag_index + 1])
            else:
                downside_risk = 0
            downside_risk_list.append(downside_risk)
        return downside_risk_list

    def get_sortino_ratio(self, strategy_year_yield, downside_risk):
        sortino_ratio_list = []
        for timetag_index in range(len(Environment.benchmark_index)):
            if downside_risk[timetag_index] > 0:
                sortino_ratio = (strategy_year_yield[timetag_index] - 3.0) / downside_risk[timetag_index]
            else:
                sortino_ratio = 0
            sortino_ratio_list.append(sortino_ratio)
        return sortino_ratio_list

    def get_tracking_error(self, benchmark_net_asset_value, strategy_net_asset_value):
        benchmark_net_asset_value_change = np.array([0]) + (
                np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
        strategy_net_asset_value_change = np.array([0]) + (
                np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
        benchmark_strategy_diff = benchmark_net_asset_value_change - strategy_net_asset_value_change
        # print(benchmark_strategy_diff)
        tracking_error_list = []
        for timetag_index in range(len(strategy_net_asset_value)):
            if timetag_index > 0:
                tracking_error = math.sqrt(252) * np.std(benchmark_strategy_diff[:timetag_index + 1])
            else:
                tracking_error = 0
            tracking_error_list.append(tracking_error)
        return tracking_error_list

    def get_information_ratio(self, benchmark_year_yield, strategy_year_yield, tracking_error):
        information_ratio_list = []
        for timetag_index in range(len(strategy_year_yield)):
            if tracking_error[timetag_index] > 0:
                information_ratio = (strategy_year_yield[timetag_index] - benchmark_year_yield[timetag_index]) / \
                                    tracking_error[timetag_index]
            else:
                information_ratio = 0
            information_ratio_list.append(information_ratio)
        return information_ratio_list

    def get_max_drawdown(self, strategy_net_asset_value):
        drawdown_list = []
        for timetag_index in range(len(strategy_net_asset_value)):
            if timetag_index > 0 and max(strategy_net_asset_value[:timetag_index]):
                drawdown = 1 - strategy_net_asset_value[timetag_index] / max(strategy_net_asset_value[:timetag_index])
            else:
                drawdown = 0
            drawdown_list.append(drawdown)

        max_drawdown_list = []
        for timetag_index in range(len(drawdown_list)):
            if timetag_index > 0:
                max_drawdown = 100 * max(drawdown_list[:timetag_index + 1])
            else:
                max_drawdown = 0
            max_drawdown_list.append(max_drawdown)

        return max_drawdown_list
