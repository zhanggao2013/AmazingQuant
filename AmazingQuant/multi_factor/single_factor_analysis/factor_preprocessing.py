# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : factor_preprocessing.py
# @Project : AmazingQuant
# ------------------------------
"""
因子数据预处理
1.数据筛选
    (1)时间区间过滤
    (2)股票池过滤

2.去极值
   (1) std法
   (2) MAD法,Median Absolute Deviation 绝对值差中位数法
   (3) 百分位法
   (4) Boxplot法

3.中性化
    市值、行业因子作为解释变量做线性回归,取残差作为新的单因子值
    行业中性时,如果没有所属行业,则因子值为空值

4.补空值(可不做)
    个股所处行业均值
    所有股票的均值
    中位数

5.标准化
    (1) 最小-最大值差标准化
    (2) Z-score标准化,
    (3) 排序百分位,标准化成均匀分布
"""
import math
from datetime import datetime

import pandas as pd
import numpy as np
import statsmodels.api as sm

from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.multi_factor.multi_factor_constant import ExtremeMethod, ScaleMethod


class FactorPreProcessing(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def data_filter(self, start=datetime(2010, 1, 1), end=datetime.now(), stock_list=None):
        if stock_list is None:
            self.raw_data = self.raw_data.loc[start: end]
        else:
            self.raw_data = self.raw_data.reindex(columns=stock_list).loc[start: end]
        return self.raw_data

    def extreme_processing(self, method=None):
        if method is None:
            method = dict(std={'sigma_multiple': 3})
        extreme_obj = Extreme(self.raw_data)
        if ExtremeMethod.STD.value in method:
            self.raw_data = extreme_obj.std_method(method['std']['sigma_multiple'])
        elif ExtremeMethod.MAD.value in method:
            self.raw_data = extreme_obj.mad_method(method['mad']['median_multiple'])
        elif ExtremeMethod.QUANTILE.value in method:
            self.raw_data = extreme_obj.quantile_method(method['quantile']['quantile_min'],
                                                        method['quantile']['quantile_max'])
        elif ExtremeMethod.BOX_PLOT.value in method:
            self.raw_data = extreme_obj.box_plot_method()
        else:
            raise Exception('This extreme method is invalid!')

        return self.raw_data

    def scale_processing(self, method=None):
        if method is None:
            method = ScaleMethod.Z_SCORE.value
        scale_obj = Scale(self.raw_data)
        if ScaleMethod.MIN_MAX.value in method:
            self.raw_data = scale_obj.min_max_method()
        elif ScaleMethod.Z_SCORE.value in method:
            self.raw_data = scale_obj.z_score_method()
        elif ScaleMethod.RANK.value in method:
            self.raw_data = scale_obj.rank_method()
        else:
            raise Exception('This scale method is invalid!')
        return self.raw_data


class Extreme(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def std_method(self, sigma_multiple):
        raw_data_mean = self.raw_data.mean(axis=1)
        raw_data_std = self.raw_data.std(axis=1)
        raw_data_max = raw_data_mean + sigma_multiple * raw_data_std
        raw_data_min = raw_data_mean - sigma_multiple * raw_data_std
        return self.raw_data.clip(raw_data_min, raw_data_max, axis=0)

    def mad_method(self, median_multiple):
        raw_data_median = self.raw_data.median(axis=1)
        raw_data_median_deviation = self.raw_data.sub(raw_data_median, axis=0)
        raw_data_mad = raw_data_median_deviation.median(axis=1)
        raw_data_max = raw_data_median + median_multiple * raw_data_mad
        raw_data_min = raw_data_median - median_multiple * raw_data_mad
        return self.raw_data.clip(raw_data_min, raw_data_max, axis=0)

    def quantile_method(self, quantile_min=0.025, quantile_max=0.975):
        raw_data_min = self.raw_data.quantile(quantile_min, axis=1)
        raw_data_max = self.raw_data.quantile(quantile_max, axis=1)
        return self.raw_data.clip(raw_data_min, raw_data_max, axis=0)

    def box_plot_method(self, quantile_min=0.25, quantile_max=0.75):
        raw_data_median = self.raw_data.median(axis=1)
        quantile_min = self.raw_data.quantile(quantile_min, axis=1)
        quantile_max = self.raw_data.quantile(quantile_max, axis=1)
        iqr = quantile_max - quantile_min

        def mc_time_tag(x, raw_data_median):
            print(x.name)
            less_median = np.tile(x[0], (len(x[1]), 1))
            greater_median = np.tile(x[1], (len(x[0]), 1)).T
            x_add = less_median + greater_median - 2 * raw_data_median[x.name]
            x_sub = less_median - greater_median
            x_add = np.array(x_add).flatten()
            x_sub = np.array(x_sub).flatten()
            mc = x_add / x_sub
            mc = mc[~np.isnan(mc)]
            return np.median(mc)

        x_less_median = self.raw_data.apply(lambda x: x[x <= raw_data_median[x.name]].values, axis=1)
        x_greater_median = self.raw_data.apply(lambda x: x[x >= raw_data_median[x.name]].values, axis=1)
        mc_series = pd.DataFrame([x_less_median, x_greater_median]).apply(mc_time_tag, args=(raw_data_median,))
        min_multiple = mc_series.apply(lambda x: -4 if x < 0 else -3.5).mul(mc_series)
        max_multiple = mc_series.apply(lambda x: 3.5 if x < 0 else 4).mul(mc_series)
        raw_data_min = quantile_min - 1.5 * min_multiple.rpow(math.e)
        raw_data_max = quantile_max - 1.5 * max_multiple.rpow(math.e)
        return self.raw_data.clip(raw_data_min, raw_data_max, axis=0)


class Scale(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def min_max_method(self):
        raw_data_min = self.raw_data.min(axis=1)
        raw_data_max = self.raw_data.max(axis=1)
        raw_data_max_min = raw_data_max - raw_data_min
        return self.raw_data.sub(raw_data_min, axis=0).div(raw_data_max_min, axis=0)

    def z_score_method(self):
        raw_data_std = self.raw_data.std(axis=1)
        raw_data_mean = self.raw_data.mean(axis=1)
        return self.raw_data.sub(raw_data_mean, axis=0).div(raw_data_std, axis=0)

    def rank_method(self):
        raw_data_rank = self.raw_data.rank(axis=1)
        return raw_data_rank.div(self.raw_data.shape[1] - self.raw_data.isna().sum(axis=1), axis=0)


class Neutralize(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def industry_method(self):
        pass

    def market_value_method(self):
        pass


if __name__ == '__main__':
    indicator_data = SaveGetIndicator().get_indicator('ma5')

    factor_pre_obj = FactorPreProcessing(indicator_data)
    data_filter = factor_pre_obj.data_filter()
    # extreme_data = factor_pre_obj.extreme_processing(dict(std={'sigma_multiple': 3}))
    extreme_data = factor_pre_obj.extreme_processing(dict(mad={'median_multiple': 3}))
    #
    # extreme_data = factor_pre_obj.extreme_processing(dict(quantile={'quantile_min': 0.025, 'quantile_max': 0.975}))
    # extreme_data = factor_pre_obj.extreme_processing(dict(box_plot={'median_multiple': 3}))
    scale_data = factor_pre_obj.scale_processing('min_max')

