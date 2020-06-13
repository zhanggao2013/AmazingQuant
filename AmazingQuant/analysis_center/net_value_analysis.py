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


class NetValueAnalysis(object):
    def __init__(self, net_value_df, benchmark_df, start_time, end_time):
        self.net_value_df = net_value_df.loc[start_time: end_time]
        self.benchmark_df = benchmark_df.loc[start_time: end_time]
        pass


class CalBullBear(object):
    """
    class :CalBullBear
    """

    def __init__(self, index_close, trade_date):
        self.index_close = index_close
        self.timetag_list = list(trade_date)
        self.bull_bear = np.array([0])

    def refx(self, data, n):
        """
        取data后n个周期的数据

        Parameters
        ----------
        data:np.array
            close
        n:int
            前n个周期

        Returns
        -------
        np.array

        """
        return np.append(data[n:], np.array([data[-1]] * n))

    def hhv(self, data, n):
        """
        取data前n个周期的最大值
        Parameters
        ----------
        data:np.array
            close
        n:int
            前n个周期

        Returns
        -------
        np.array
        """
        data_length = len(data)
        hhv_data = np.array([])
        if data_length > 0:
            hhv_data = np.array([data[0]])
            for i in range(1, min(n, data_length)):
                hhv_data = np.append(hhv_data, np.max(data[: i]))
            hhv_data = np.append(hhv_data, pd.Series(data[:-1]).rolling(n).max().dropna().tolist())
        return hhv_data

    def llv(self, data, n):
        """
        取data前n个周期的最小值
        Parameters
        ----------
        data:np.array
            close
        n:int
            前n个周期

        Returns
        -------
        np.array
        """
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
        return


class NetValueIndicator(object):
    """
    class:净值类指标计算
    """

    def __init__(self, net_value, index_close, trade_date, backtesting_day_num=252):
        """
        Parameters
        ----------
        net_value:np.array
            净值
        index_close:np.array
            基准净值
        trade_date:np.array
            交易日列表
        backtesting_day_num:int
            计算最近多少个交易日
        """
        self.backtesting_day_num = backtesting_day_num
        self.net_value = net_value[-self.backtesting_day_num:]
        self.index_close = index_close[-self.backtesting_day_num:]
        self.trade_date = trade_date[-self.backtesting_day_num:]
        self.bull_bear = CalBullBear(self.index_close, self.trade_date).get_index_bull_bear()

        self.net_value_ratio = np.array([])
        self.index_close_ratio = np.array([])
        self.net_year_yield = np.array([])
        self.index_year_yield = np.array([])

        self.year_volatility_array = np.array([])
        self.beta_array = np.array([])
        self.alpha_array = np.array([])
        self.sharp_array = np.array([])
        self.drawdown_array = np.array([])
        self.max_drawdown_array = np.array([])
        self.max_drawdown_end_date = ""
        self.max_drawdown_start_date = ""
        self.bull_win_index_ratio = 0
        self.bear_win_index_ratio = 0
        self.day_ratio_distribution = {"-10%以下": 0, "-10%~-5%": 0, "-5%~-3%": 0, "-3%~-2%": 0, "-2%~-1%": 0,
                                       "-1%~0%": 0,
                                       "0%~1%": 0, "1%~2%": 0, "2%~3%": 0, "3%~5%": 0, "5%~10%": 0, "10%以上": 0}
        self.day_ratio_average = 0
        self.month_ratio = {}
        self.month_ratio_average = 0
        self.day_volatility = 0
        self.month_volatility = 0
        self.selection_ability = 0
        self.timing_ability = 0

    def get_net_value(self, close):
        return np.array([close[i] / close[0] for i in range(len(close))])

    def get_profit_ratio(self, close):
        return np.insert(100 * (close[1:] / close[:-1] - 1), 0, 0)

    def get_year_volatility(self):
        for index in range(len(self.net_value_ratio)):
            if index > 0:
                volatility = math.sqrt(252) * np.std(self.net_value_ratio[:index + 1])
            else:
                volatility = 0
            self.year_volatility_array = np.append(self.year_volatility_array, volatility)
        return self.year_volatility_array

    def get_year_yield(self, close):
        return np.array([100 * (pow(close[index], 252.0 / (index + 1)) - 1) for index in range(len(close))])

    def get_beta(self):
        for i in range(len(self.index_close)):
            if i > 0:
                beta = (np.cov(self.net_value_ratio, self.index_close_ratio)[0, 1]) / np.var(self.index_close_ratio)
            else:
                beta = 0
            self.beta_array = np.append(self.beta_array, beta)
        return self.beta_array

    def get_alpha(self):
        for i in range(len(self.index_year_yield)):
            alpha = self.net_year_yield[i] - (3.0 + self.beta_array[i] * (self.index_year_yield[i] - 3.0))
            self.alpha_array = np.append(self.alpha_array, alpha)
        return self.alpha_array

    def get_sharp(self):
        for index in range(len(self.net_year_yield)):
            if self.year_volatility_array[index] > 0:
                sharp = (self.net_year_yield[index] - 3.0) / self.year_volatility_array[index]
            else:
                sharp = 0
            self.sharp_array = np.append(self.sharp_array, sharp)
        return self.sharp_array

    def get_max_drawdown(self):
        for timetag_index in range(len(self.net_value)):
            if timetag_index > 0:
                drawdown = 1 - self.net_value[timetag_index] / max(self.net_value[:timetag_index + 1])
            else:
                drawdown = 0
            self.drawdown_array = np.append(self.drawdown_array, drawdown)
        for timetag_index in range(len(self.drawdown_array)):
            if timetag_index > 0:
                max_drawdown = 100 * max(self.drawdown_array[:timetag_index + 1])
            else:
                max_drawdown = 0
            self.max_drawdown_array = np.append(self.max_drawdown_array, max_drawdown)
        max_drawdown_end_index = np.argmax(self.drawdown_array)
        max_drawdown_start_index = 0
        for i in range(len(self.drawdown_array)):
            if self.drawdown_array[i] == 0 and i < max_drawdown_end_index:
                max_drawdown_start_index = i
        self.max_drawdown_end_date = self.trade_date[np.argmax(self.drawdown_array)]
        self.max_drawdown_start_date = self.trade_date[max_drawdown_start_index]
        return self.drawdown_array, self.max_drawdown_array, self.max_drawdown_start_date, self.max_drawdown_end_date

    def get_win_index_ratio(self):
        index = 0
        bull_win_num = 0
        bear_win_num = 0
        for x in np.nditer(self.bull_bear):
            if x == 0 and self.net_value_ratio[index] > self.index_close_ratio[index]:
                bull_win_num += 1
            if x == 1 and self.net_value_ratio[index] > self.index_close_ratio[index]:
                bear_win_num += 1
            index += 1
        self.bull_win_index_ratio = bull_win_num / np.sum(self.bull_bear) * 100
        self.bear_win_index_ratio = bear_win_num / (self.backtesting_day_num - np.sum(self.bull_bear)) * 100
        return self.bull_win_index_ratio, self.bear_win_index_ratio

    def get_day_win_ratio(self):
        return np.sum(self.net_value_ratio >= 0) / self.backtesting_day_num

    def get_day_ratio_distribution(self):
        self.day_ratio_distribution = {"-10%以下": np.sum(self.net_value_ratio < -10),
                                       "-10%~-5%": np.sum((self.net_value_ratio >= -10) & (self.net_value_ratio < -5)),
                                       "-5%~-3%": np.sum((self.net_value_ratio >= -5) & (self.net_value_ratio < -3)),
                                       "-3%~-2%": np.sum((self.net_value_ratio >= -3) & (self.net_value_ratio < -2)),
                                       "-2%~-1%": np.sum((self.net_value_ratio >= -2) & (self.net_value_ratio < -1)),
                                       "-1%~0%": np.sum((self.net_value_ratio >= -1) & (self.net_value_ratio < 0)),
                                       "0%~1%": np.sum((self.net_value_ratio >= 0) & (self.net_value_ratio < 1)),
                                       "1%~2%": np.sum((self.net_value_ratio >= 1) & (self.net_value_ratio < 2)),
                                       "2%~3%": np.sum((self.net_value_ratio >= 2) & (self.net_value_ratio < 3)),
                                       "3%~5%": np.sum((self.net_value_ratio >= 3) & (self.net_value_ratio < 5)),
                                       "5%~10%": np.sum((self.net_value_ratio >= 5) & (self.net_value_ratio < 10)),
                                       "10%以上": np.sum(self.net_value_ratio >= 10), }
        self.day_ratio_distribution = {key: 100 * value / self.backtesting_day_num for key, value in
                                       self.day_ratio_distribution.items()}

    def get_day_ratio_average(self):
        self.day_ratio_average = 100 * np.mean(self.net_value_ratio)

    def get_month_ratio(self):
        for i in range(len(self.trade_date) - 1):
            if self.trade_date[i][:-2] in self.month_ratio.keys():
                self.month_ratio[self.trade_date[i][:-2]].append(self.net_value[i])
            else:
                self.month_ratio[self.trade_date[i][:-2]] = [self.net_value[i]]
        self.month_ratio = {key: 100 * (value[-1] / value[0] - 1) for key, value in self.month_ratio.items()}

    def get_month_ratio_average(self):
        self.month_ratio_average = sum(self.month_ratio.values()) / len(self.month_ratio.values())

    def get_day_volatility(self):
        self.day_volatility = np.std(self.net_value_ratio)

    def get_month_volatility(self):
        self.month_volatility = np.std(list(self.month_ratio.values()))

    def get_selection_timing(self):
        self.selection_ability = 0
        self.timing_ability = 0
        rf = 0.03 / 252
        excess_rate = self.net_value_ratio - rf
        coe_beta1 = self.index_close_ratio - rf

        coe_beta2_HM = np.multiply(coe_beta1, coe_beta1 > 0)
        X_HM = pd.DataFrame({'coe1': coe_beta1, 'coe2': coe_beta2_HM})
        X_HM = sm.add_constant(X_HM)
        estimate_HM = sm.OLS(excess_rate, X_HM).fit()
        print("HM模型结果", estimate_HM.params, estimate_HM.pvalues, estimate_HM.tvalues, estimate_HM.rsquared)

        coe_beta2_TM = coe_beta1 ** 2
        X_TM = pd.DataFrame({'coe1': coe_beta1, 'coe2': coe_beta2_TM})
        X_TM = sm.add_constant(X_TM)
        estimate_TM = sm.OLS(excess_rate, X_TM).fit()
        print("TM模型结果", estimate_TM.params, estimate_TM.pvalues, estimate_TM.tvalues, estimate_TM.rsquared)

        coe_beta1_CL = np.multiply(coe_beta1, coe_beta1 > 0)
        coe_beta2_CL = np.multiply(coe_beta1, coe_beta1 < 0)
        X_CL = pd.DataFrame({'coe1': coe_beta1_CL, 'coe2': coe_beta2_CL})
        X_CL = sm.add_constant(X_CL)
        estimate_CL = sm.OLS(excess_rate, X_CL).fit()
        print("CL模型结果", estimate_CL.params, estimate_CL.pvalues, estimate_CL.tvalues, estimate_CL.rsquared)

    def process(self):
        self.net_value = self.get_net_value(self.net_value)
        self.index_close = self.get_net_value(self.index_close)
        self.net_value_ratio = self.get_profit_ratio(self.net_value)
        self.index_close_ratio = self.get_profit_ratio(self.index_close)
        self.net_year_yield = self.get_year_yield(self.net_value)
        self.index_year_yield = self.get_year_yield(self.index_close)

        self.get_year_volatility()
        self.get_beta()
        self.get_alpha()
        self.get_sharp()
        self.get_max_drawdown()
        self.get_win_index_ratio()
        self.get_day_win_ratio()
        self.get_day_ratio_distribution()
        self.get_day_ratio_average()
        self.get_month_ratio()
        self.get_month_ratio_average()
        self.get_day_volatility()
        self.get_month_volatility()
        self.get_selection_timing()


if __name__ == '__main__':
    start_time = datetime(2010, 1, 4)
    end_time = datetime(2019, 11, 4)
    kline_object = GetKlineData()
    #
    # 指数行情，沪深300代替
    all_index_data = kline_object.cache_all_index_data()
    benchmark_df = kline_object.get_market_data(all_index_data, stock_code=['000300.SH'],
                                                field=['close'], start=start_time, end=end_time)
    # 策略精致，上证指数代替
    net_value_df = kline_object.get_market_data(all_index_data, stock_code=['000001.SH'],
                                                field=['close'], start=start_time, end=end_time)

    net_value_analysis_obj = NetValueAnalysis(net_value_df, benchmark_df, start_time, end_time)


