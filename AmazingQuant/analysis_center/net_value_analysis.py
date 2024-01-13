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
                            'total_balance', 'available' columns必须有，index为datetime的日线级别时间序列
        :param benchmark_df: columns=['close', 'net_value', 'profit_ratio', 'drawdown']，closecolumns必须有，
                            index为datetime的日线级别时间序列
        :param start_time: datetime
        :param end_time: datetime
        """
        if max(benchmark_df.index) < end_time:
            raise Exception('max(benchmark_df.index) < end_time')
        if min(benchmark_df.index) > start_time:
            raise Exception('min(benchmark_df.index) > start_time:')
        if max(net_value_df.index) < end_time:
            raise Exception('max(net_value_df.index) < end_time')
        if min(net_value_df.index) > start_time:
            raise Exception('min(net_value_df.index) > start_time')
        # 净值'net_value', 日收益率'profit_ratio', 总资产'total_balance', 可用资金'available', 最大回撤'drawdown'
        self.net_value_df = net_value_df.loc[start_time: end_time]
        # 基准收盘价'close', 基准净值'net_value', 基准收益率'profit_ratio', 最大回撤'drawdown'
        self.benchmark_df = benchmark_df.loc[start_time: end_time]

    def cal_net_value(self):
        self.net_value_df.insert(loc=0, column='net_value',
                                 value=self.net_value_df['total_balance'] / self.net_value_df['total_balance'].iloc[0])
        self.benchmark_df.insert(loc=0, column='net_value',
                                 value=self.benchmark_df['close'] / self.benchmark_df['close'].iloc[0])

    def cal_capital_utilization(self):
        capital_utilization = 100 * (self.net_value_df['total_balance'] - self.net_value_df['available']) / \
                                self.net_value_df['total_balance']
        self.net_value_df.insert(loc=0, column='capital_utilization', value=capital_utilization)

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
        sharpe = None
        if net_year_volatility != 0:
            sharpe = (net_year_yield - 3.0) / net_year_volatility
        return sharpe

    @staticmethod
    def cal_tracking_error(net_value_ratio, benchmark_close_ratio):
        net_index_diff = benchmark_close_ratio - net_value_ratio
        return math.sqrt(252) * np.std(net_index_diff)

    @staticmethod
    def cal_information_ratio(net_year_yield, benchmark_year_yield, tracking_error):
        information_ratio = None
        if tracking_error != 0:
            information_ratio = (net_year_yield - benchmark_year_yield) / tracking_error
        return information_ratio

    @staticmethod
    def cal_downside_risk(net_value_ratio):
        downside_net_value_ratio = [net_value_ratio[i] if net_value_ratio[i] < 3.0 / 252 else 0 for i in
                                    range(len(net_value_ratio))]
        return math.sqrt(252) * np.std(downside_net_value_ratio)

    @staticmethod
    def cal_sortino_ratio(net_year_yield, downside_risk):
        sortino_ratio = None
        if downside_risk != 0:
            sortino_ratio = (net_year_yield - 3.0) / downside_risk
        return sortino_ratio

    @staticmethod
    def cal_calmar_ratio(net_year_yield, max_drawdown):
        calmar_ratio = None
        if abs(max_drawdown) != 0:
            calmar_ratio = (net_year_yield - 3.0) / abs(max_drawdown)
        return calmar_ratio

    @staticmethod
    def cal_treynor_ratio(net_year_yield, beta):
        treynor_ratio = None
        if beta != 0:
            treynor_ratio = (net_year_yield - 3.0) / beta
        return treynor_ratio

    @staticmethod
    def cal_max_drawdown(drawdown_series):
        return drawdown_series.min()

    @staticmethod
    def cal_day_win_ratio(profit_ratio):
        return np.sum(profit_ratio >= 0) / len(profit_ratio)*100

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
        month_first = net_value_series.resample('MS').first()
        month_last = net_value_series.resample('M').last()
        month_ratio_series = month_last.pct_change()
        month_ratio_series.iloc[0] = (month_last.iloc[0] - month_first.iloc[0])/month_first.iloc[0]
        month_ratio = {str(date_index.year * 100 + date_index.month): month_ratio_series[date_index]*100
                       for date_index in month_ratio_series.index}
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

    @staticmethod
    def cal_skew_kurt(profit_ratio):
        """
        :param profit_ratio:
        :return: Skewness, Kurtosis,偏度 峰度
        """
        return profit_ratio.skew(), profit_ratio.kurt()

    def cal_net_analysis_result(self):
        net_analysis_result = {}
        self.cal_net_value()
        self.cal_profit_ratio()
        self.cal_drawdown()
        self.cal_capital_utilization()
        net_analysis_result['net_value_df'] = self.net_value_df
        net_analysis_result['benchmark_df'] = self.benchmark_df
        # 年化收益率
        net_year_yield = self.cal_year_yield(self.net_value_df['net_value'])
        net_analysis_result['net_year_yield'] = net_year_yield
        benchmark_year_yield = self.cal_year_yield(self.benchmark_df['net_value'])
        net_analysis_result['benchmark_year_yield'] = benchmark_year_yield
        # 年化波动率
        net_year_volatility = self.cal_year_volatility(
            self.net_value_df['profit_ratio'])
        net_analysis_result['net_year_volatility'] = net_year_volatility
        benchmark_year_volatility = self.cal_year_volatility(
            self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_year_volatility'] = benchmark_year_volatility

        # 历史最大回撤
        net_max_drawdown = self.cal_max_drawdown(self.net_value_df['drawdown'])
        net_analysis_result['net_max_drawdown'] = net_max_drawdown
        benchmark_max_drawdown = self.cal_max_drawdown(self.benchmark_df['drawdown'])
        net_analysis_result['benchmark_max_drawdown'] = benchmark_max_drawdown

        # 日波动率
        net_day_volatility = self.cal_day_volatility(self.net_value_df['profit_ratio'])
        net_analysis_result['net_day_volatility'] = net_day_volatility
        benchmark_day_volatility = self.cal_day_volatility(
            self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_day_volatility'] = benchmark_day_volatility

        # beta
        beta = self.cal_beta(self.net_value_df['profit_ratio'],
                             self.benchmark_df['profit_ratio'])
        net_analysis_result['beta'] = beta
        # alpha
        alpha = self.cal_alpha(net_year_yield, benchmark_year_yield, beta)
        net_analysis_result['alpha'] = alpha
        # sharpe
        sharpe = self.cal_sharpe(net_year_yield, net_year_volatility)
        net_analysis_result['sharpe'] = sharpe
        # 跟踪误差
        tracking_error = self.cal_tracking_error(self.net_value_df['profit_ratio'],
                                                 self.benchmark_df['profit_ratio'])
        net_analysis_result['tracking_error'] = tracking_error
        # 信息比率
        information_ratio = self.cal_information_ratio(net_year_yield,
                                                       benchmark_year_yield,
                                                       tracking_error)
        net_analysis_result['information_ratio'] = information_ratio
        # 下行风险
        downside_risk = self.cal_downside_risk(self.net_value_df['profit_ratio'])
        net_analysis_result['downside_risk'] = downside_risk

        benchmark_downside_risk = self.cal_downside_risk(self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_downside_risk'] = benchmark_downside_risk

        # 索提诺比率
        sortino_ratio = self.cal_sortino_ratio(net_year_yield, downside_risk)
        net_analysis_result['sortino_ratio'] = sortino_ratio

        # 特雷诺比率
        treynor_ratio = self.cal_treynor_ratio(net_year_yield, beta)
        net_analysis_result['treynor_ratio'] = treynor_ratio

        # calmar_ratio
        calmar_ratio = self.cal_calmar_ratio(net_year_yield, net_max_drawdown)
        net_analysis_result['calmar_ratio'] = calmar_ratio

        bull_win_index_ratio, bear_win_index_ratio = self.cal_win_index_ratio()
        net_analysis_result['bull_win_index_ratio'] = bull_win_index_ratio
        net_analysis_result['bear_win_index_ratio'] = bear_win_index_ratio

        # 日胜率
        net_day_win_ratio = self.cal_day_win_ratio(self.net_value_df['profit_ratio'])
        net_analysis_result['net_day_win_ratio'] = net_day_win_ratio
        benchmark_day_win_ratio = self.cal_day_win_ratio(self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_day_win_ratio'] = benchmark_day_win_ratio

        # 日收益率分布
        net_day_ratio_distribution = self.cal_day_ratio_distribution(
            self.net_value_df['profit_ratio'])
        net_analysis_result['net_day_ratio_distribution'] = net_day_ratio_distribution
        benchmark_day_ratio_distribution = self.cal_day_ratio_distribution(
            self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_day_ratio_distribution'] = benchmark_day_ratio_distribution

        # 日均收益率
        net_day_ratio_average = self.cal_day_ratio_average(
            self.net_value_df['profit_ratio'])
        net_analysis_result['net_day_ratio_average'] = net_day_ratio_average
        benchmark_day_ratio_average = self.cal_day_ratio_average(
            self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_day_ratio_average'] = benchmark_day_ratio_average

        # 月度收益率
        net_month_ratio = self.cal_month_ratio(self.net_value_df['net_value'])
        net_analysis_result['net_month_ratio'] = net_month_ratio
        benchmark_month_ratio = self.cal_month_ratio(self.benchmark_df['net_value'])
        net_analysis_result['benchmark_month_ratio'] = benchmark_month_ratio
        # 月均收益率
        net_month_ratio_average = self.cal_month_ratio_average(net_month_ratio)
        net_analysis_result['net_month_ratio_average'] = net_month_ratio_average
        benchmark_month_ratio_average = self.cal_month_ratio_average(benchmark_month_ratio)
        net_analysis_result['benchmark_month_ratio_average'] = benchmark_month_ratio_average

        # 月收益波动率
        net_month_volatility = self.cal_month_volatility(net_month_ratio)
        net_analysis_result['net_month_volatility'] = net_month_volatility
        benchmark_month_volatility = self.cal_month_volatility(benchmark_month_ratio)
        net_analysis_result['benchmark_month_volatility'] = benchmark_month_volatility

        # 偏度，峰度
        net_skewness, net_kurtosis = self.cal_skew_kurt(
            self.net_value_df['profit_ratio'])
        net_analysis_result['net_skewness'] = net_skewness
        net_analysis_result['net_kurtosis'] = net_kurtosis
        benchmark_skewness, benchmark_kurtosis = self.cal_skew_kurt(
            self.benchmark_df['profit_ratio'])
        net_analysis_result['benchmark_skewness'] = benchmark_skewness
        net_analysis_result['benchmark_kurtosis'] = benchmark_kurtosis
        return net_analysis_result


if __name__ == '__main__':
    start_time = datetime(2018, 1, 2)
    end_time = datetime(2018, 12, 28)
    kline_object = GetKlineData()
    #
    # 指数行情，沪深300代替
    all_index_data = kline_object.cache_all_index_data()
    benchmark_df = kline_object.get_market_data(all_index_data, stock_code=['000300.SH'], field=['close'], ) \
        .to_frame(name='close')

    # 策略净值数据,index 为 datetime,取单个账户分析，后续可做多个账户
    net_value_df = pd.read_csv('account_data.csv', index_col=0)
    net_value_df.index = pd.DatetimeIndex(net_value_df.index)
    net_value_single_account_df = pd.DataFrame({})
    for i in net_value_df.groupby('account_id'):
        net_value_single_account_df = i[1]
        break
    a = net_value_single_account_df.resample('MS').first()
    b = net_value_single_account_df.resample('M').last()
    # net_value_analysis_obj = NetValueAnalysis(net_value_single_account_df, benchmark_df, start_time, end_time)
    #
    # net_analysis_result = net_value_analysis_obj.cal_net_analysis_result()
