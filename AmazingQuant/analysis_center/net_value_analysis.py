# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/16
# @Author  : gao
# @File    : net_value_analysis.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime
import math

import pandas as pd
import numpy as np
import statsmodels.api as sm

from AmazingQuant.data_center.api_data.get_kline import GetKlineData


class CalBullBear(object):
    """
    class :CalBullBear
    """

    def __init__(self, index_close):
        self.index_close = index_close
        self.bull_bear = np.array([0])

    def refx(self, data, n):
        return np.append(data[n:], np.array([data[-1]] * n))

    def hhv(self, data, n):
        data_length = len(data)
        hhv_data = np.array([])
        if data_length > 0:
            hhv_data = np.array([data[0]])
            for i in range(1, min(n, data_length)):
                hhv_data = np.append(hhv_data, np.max(data[: i]))
            hhv_data = np.append(hhv_data, pd.Series(data[:-1]).rolling(n).max().dropna().tolist())
        return hhv_data

    def llv(self, data, n):
        data_length = len(data)
        llv_data = np.array([])
        if data_length > 0:
            llv_data = np.array([data[0]])
            for i in range(1, min(n, data_length)):
                llv_data = np.append(llv_data, np.min(data[: i]))
            llv_data = np.append(llv_data, pd.Series(data[:-1]).rolling(n).min().dropna().tolist())
        return llv_data

    def get_index_bull_bear(self):
        """
        根据指数判断牛熊，1代表"熊", 0代表"牛"
        Returns
        -------
        np.array
        """
        n = 20
        future_close = self.refx(self.index_close, n)
        hhv_future = self.hhv(future_close, n)
        llv_future = self.llv(future_close, n)
        top_point = 0
        low_point = self.index_close[0]
        index = 0

        for close in np.nditer(self.index_close):
            if top_point < hhv_future[index]:
                top_point = hhv_future[index]
            if low_point > llv_future[index]:
                low_point = llv_future[index]
            if close >= top_point:
                low_point = close
            if close <= low_point:
                top_point = close
            if self.bull_bear[-1] == 0 and close >= top_point:
                if index == 0:
                    self.bull_bear = np.array([1])
                else:
                    self.bull_bear = np.append(self.bull_bear, 1)
                    # print("熊", 1, index)
            elif self.bull_bear[-1] == 1 and close <= low_point:
                self.bull_bear = np.append(self.bull_bear, 0)
                # print("牛", 0, index)
            elif index > 0:
                self.bull_bear = np.append(self.bull_bear, self.bull_bear[-1])
                # print("延续前值", bull_bear[-1], index)
            index += 1
        # bull-0  bear-1
        return self.bull_bear


class NetValueAnalysis(object):
    def __init__(self, net_value_df, benchmark_df, start_time, end_time):
        """
        net_value_df和benchmark_df的index必须在【start_time, end_time】
        :param net_value_df:  columns=['total_balance', 'available', 'net_value', 'profit_ratio', 'drawdown']
        :param benchmark_df: columns=['close', 'net_value', 'profit_ratio', 'drawdown']
        :param start_time:
        :param end_time:
        """
        # 净值'net_value', 日收益率'profit_ratio', 总资产'total_balance', 可用资金'available', 最大回撤'drawdown'
        self.net_value_df = net_value_df.loc[start_time: end_time]
        # 基准收盘价'close', 基准净值'net_value', 基准收益率'profit_ratio', 最大回撤'drawdown'
        self.benchmark_df = benchmark_df.loc[start_time: end_time]

        # 截面数据指标
        # 年化收益率
        self.net_year_yield = None

        # 基准年化收益率
        self.benchmark_year_yield = None

        # 年化波动率
        self.year_volatility = None

        # 基准年化波动率
        self.benchmark_year_volatility = None

        # beta
        self.beta = None

        # alpha
        self.alpha = None

        # sharpe
        self.sharp = None

        # 历史最大回撤
        self.max_drawdown = None

        # 上涨区间胜率
        self.bull_win_index_ratio = None

        # 下跌区间胜率
        self.bear_win_index_ratio = None

        # 日收益率分布
        self.day_ratio_distribution = {"-10%以下": 0, "-10%~-5%": 0, "-5%~-3%": 0, "-3%~-2%": 0, "-2%~-1%": 0,
                                       "-1%~0%": 0,
                                       "0%~1%": 0, "1%~2%": 0, "2%~3%": 0, "3%~5%": 0, "5%~10%": 0, "10%以上": 0}

        # 日均收益率
        self.day_ratio_average = None

        # 月收益率
        self.month_ratio = {}

        # 月均收益率
        self.month_ratio_average = None

        # 日收益波动率
        self.day_volatility = None

        # 月收益率波动率
        self.month_volatility = None
        # HM模型
        self.HM_model = {'selection': None, 'timing': None, 'p_value': None, }

        # TM模型
        self.TM_model = {'selection': None, 'timing': None, 'p_value': None, }

        # HM模型
        self.CL_model = {'selection': None, 'timing': None, 'p_value': None, }

    def cal_net_value(self):
        self.net_value_df.insert(loc=0, column='net_value',
                                 value=self.net_value_df['total_balance'] / self.net_value_df['total_balance'].iloc[0])
        self.benchmark_df.insert(loc=0, column='net_value',
                                 value=self.benchmark_df['close'] / self.benchmark_df['close'].iloc[0])

    def cal_profit_ratio(self):
        self.net_value_df.insert(loc=0, column='profit_ratio', value=self.net_value_df['net_value'].pct_change() * 100)
        self.benchmark_df.insert(loc=0, column='profit_ratio', value=self.benchmark_df['net_value'].pct_change() * 100)

    def cal_drawdown(self):
        net_drawdown = (self.net_value_df['net_value']
                        .div(self.net_value_df['net_value'].expanding().max()) - 1) * 100
        self.net_value_df.insert(loc=0, column='drawdown', value=net_drawdown)

        benchmark_drawdown = (self.benchmark_df['net_value']
                              .div(self.benchmark_df['net_value'].expanding().max()) - 1) * 100
        self.benchmark_df.insert(loc=0, column='drawdown', value=benchmark_drawdown)

    def cal_win_index_ratio(self):
        bull_bear = CalBullBear(self.benchmark_df['close'].values).get_index_bull_bear()
        index = 0
        bull_win_num = 0
        bear_win_num = 0
        for x in np.nditer(bull_bear):
            if x == 0 and self.net_value_df['profit_ratio'].iloc[index] > self.benchmark_df['profit_ratio'].iloc[index]:
                bull_win_num += 1
            if x == 1 and self.net_value_df['profit_ratio'].iloc[index] > self.benchmark_df['profit_ratio'].iloc[index]:
                bear_win_num += 1
            index += 1
        self.bull_win_index_ratio = bull_win_num / (self.net_value_df.shape[0] - np.sum(bull_bear)) * 100
        self.bear_win_index_ratio = bear_win_num / np.sum(bull_bear) * 100
        return self.bull_win_index_ratio, self.bear_win_index_ratio

    @staticmethod
    def cal_year_yield(net_value_series):
        return 100 * (pow(net_value_series.iloc[-1], 245.0 / (len(net_value_series) + 1)) - 1)

    @staticmethod
    def cal_year_volatility(profit_ratio):
        return math.sqrt(245.0) * profit_ratio.std()

    @staticmethod
    def cal_beta(net_profit_ratio, benchmark_profit_ratio):
        return (np.cov(net_profit_ratio.values[1:], benchmark_profit_ratio.values[1:])[0, 1]) / \
               np.var(benchmark_profit_ratio)

    @staticmethod
    def cal_alpha(net_year_yield, benchmark_year_yield, beta):
        return net_year_yield - (3.0 + beta * (benchmark_year_yield - 3.0))

    @staticmethod
    def cal_sharpe(net_year_yield, net_year_volatility):
        return (net_year_yield - 3.0) / net_year_volatility

    @staticmethod
    def cal_max_drawdown(drawdown_series):
        return drawdown_series.min()

    @staticmethod
    def cal_day_win_ratio(profit_ratio):
        return np.sum(profit_ratio >= 0) / len(profit_ratio)

    @staticmethod
    def cal_day_ratio_distribution(profit_ratio):
        day_ratio_distribution = {"-10%以下": np.sum(profit_ratio < -10),
                                  "-10%~-5%": np.sum((profit_ratio >= -10) & (profit_ratio < -5)),
                                  "-5%~-3%": np.sum((profit_ratio >= -5) & (profit_ratio < -3)),
                                  "-3%~-2%": np.sum((profit_ratio >= -3) & (profit_ratio < -2)),
                                  "-2%~-1%": np.sum((profit_ratio >= -2) & (profit_ratio < -1)),
                                  "-1%~0%": np.sum((profit_ratio >= -1) & (profit_ratio < 0)),
                                  "0%~1%": np.sum((profit_ratio >= 0) & (profit_ratio < 1)),
                                  "1%~2%": np.sum((profit_ratio >= 1) & (profit_ratio < 2)),
                                  "2%~3%": np.sum((profit_ratio >= 2) & (profit_ratio < 3)),
                                  "3%~5%": np.sum((profit_ratio >= 3) & (profit_ratio < 5)),
                                  "5%~10%": np.sum((profit_ratio >= 5) & (profit_ratio < 10)),
                                  "10%以上": np.sum(profit_ratio >= 10), }
        day_ratio_distribution = {key: value / len(profit_ratio) for key, value in day_ratio_distribution.items()}
        return day_ratio_distribution

    @staticmethod
    def cal_day_ratio_average(profit_ratio):
        return profit_ratio.mean()

    @staticmethod
    def cal_month_ratio(net_value_series):
        month_ratio = {}
        for i in net_value_series.index:
            if str(i.year*100 + i.month) in month_ratio.keys():
                month_ratio[str(i.year*100 + i.month)].append(net_value_series[i])
            else:
                month_ratio[str(i.year*100 + i.month)] = [net_value_series[i]]

        month_ratio = {key: 100 * (value[-1] / value[0] - 1) for key, value in month_ratio.items()}
        return month_ratio

    @staticmethod
    def cal_month_ratio_average(month_ratio):
        return sum(month_ratio.values()) / len(month_ratio.values())

    @staticmethod
    def cal_day_volatility(profit_ratio):
        return np.std(profit_ratio)

    @staticmethod
    def cal_month_volatility(month_ratio):
        return np.std(list(month_ratio.values()))


if __name__ == '__main__':
    start_time = datetime(2018, 1, 2)
    end_time = datetime(2018, 12, 28)
    kline_object = GetKlineData()
    #
    # 指数行情，沪深300代替
    all_index_data = kline_object.cache_all_index_data()
    benchmark_df = kline_object.get_market_data(all_index_data, stock_code=['000300.SH'],
                                                field=['close'], start=start_time, end=end_time).to_frame(name='close')
    # 策略净值数据,index 为 datetime,取单个账户分析，后续可做多个账户
    net_value_df = pd.read_csv('account_data.csv', index_col=0)
    net_value_df.index = pd.DatetimeIndex(net_value_df.index)
    net_value_single_account_df = pd.DataFrame({})
    for i in net_value_df.groupby('account_id'):
        net_value_single_account_df = i[1]
        break

    net_value_analysis_obj = NetValueAnalysis(net_value_single_account_df, benchmark_df, start_time, end_time)
    net_value_analysis_obj.cal_net_value()
    net_value_analysis_obj.cal_profit_ratio()
    net_value_analysis_obj.cal_drawdown()

    net_year_yield = net_value_analysis_obj.cal_year_yield(net_value_analysis_obj.net_value_df['net_value'])
    benchmark_year_yield = net_value_analysis_obj.cal_year_yield(net_value_analysis_obj.benchmark_df['net_value'])

    net_year_volatility = net_value_analysis_obj.cal_year_volatility(
        net_value_analysis_obj.net_value_df['profit_ratio'])
    benchmark_year_volatility = net_value_analysis_obj.cal_year_volatility(
        net_value_analysis_obj.benchmark_df['profit_ratio'])

    net_day_volatility = net_value_analysis_obj.cal_day_volatility(net_value_analysis_obj.net_value_df['profit_ratio'])
    benchmark_day_volatility = net_value_analysis_obj.cal_day_volatility(net_value_analysis_obj.benchmark_df['profit_ratio'])

    beta = net_value_analysis_obj.cal_beta(net_value_analysis_obj.net_value_df['profit_ratio'],
                                           net_value_analysis_obj.benchmark_df['profit_ratio'])

    alpha = net_value_analysis_obj.cal_alpha(net_year_yield, benchmark_year_yield, beta)
    sharpe = net_value_analysis_obj.cal_sharpe(net_year_yield, net_year_volatility)

    net_max_drawdown = net_value_analysis_obj.cal_max_drawdown(net_value_analysis_obj.net_value_df['drawdown'])
    benchmark_max_drawdown = net_value_analysis_obj.cal_max_drawdown(net_value_analysis_obj.benchmark_df['drawdown'])

    bull_win_index_ratio, bear_win_index_ratio = net_value_analysis_obj.cal_win_index_ratio()

    net_day_win_ratio = net_value_analysis_obj.cal_day_win_ratio(net_value_analysis_obj.net_value_df['profit_ratio'])
    benchmark_day_win_ratio = net_value_analysis_obj.cal_day_win_ratio(
        net_value_analysis_obj.benchmark_df['profit_ratio'])

    net_day_ratio_distribution = net_value_analysis_obj.cal_day_ratio_distribution(
        net_value_analysis_obj.net_value_df['profit_ratio'])
    benchmark_day_ratio_distribution = net_value_analysis_obj.cal_day_ratio_distribution(
        net_value_analysis_obj.benchmark_df['profit_ratio'])

    net_day_ratio_average = net_value_analysis_obj.cal_day_ratio_average(
        net_value_analysis_obj.net_value_df['profit_ratio'])
    benchmark_day_ratio_average = net_value_analysis_obj.cal_day_ratio_average(
        net_value_analysis_obj.benchmark_df['profit_ratio'])

    net_month_ratio = net_value_analysis_obj.cal_month_ratio(net_value_analysis_obj.net_value_df['net_value'])
    benchmark_month_ratio = net_value_analysis_obj.cal_month_ratio(net_value_analysis_obj.benchmark_df['net_value'])

    net_month_ratio_average = net_value_analysis_obj.cal_month_ratio_average(net_month_ratio)
    benchmark_month_ratio_average = net_value_analysis_obj.cal_month_ratio_average(benchmark_month_ratio)

    net_month_volatility = net_value_analysis_obj.cal_month_volatility(net_month_ratio)
    benchmark_month_volatility = net_value_analysis_obj.cal_month_volatility(benchmark_month_ratio)



