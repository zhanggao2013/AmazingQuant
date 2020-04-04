# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : factor_preprocessing.py
# @Project : AmazingQuant
# ------------------------------
"""
因子数据预处理
1.去极值
   (1) std法
   (2) MAD法,Median Absolute Deviation 绝对值差中位数法
   (3) Boxplot法

2.补空值(可不做)
    个股所处行业均值
    所有股票的均值

3.中性化
    市值、行业因子作为解释变量做线性回归,取残差作为新的单因子值

4.标准化
    (1) 最小-最大利差标准化
    (2) Z-score标准化,
    (3) 排序百分位,标准化成均匀分布
"""

import pandas as pd

from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.multi_factor.multi_factor_constant import ExtremeMethod


class FactorPreProcessing(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def extreme_processing(self, method=None):
        if method is None:
            method = dict(std={'sigma_multiple': 3})
        extreme_obj = Extreme(self.raw_data)
        if ExtremeMethod.STD.value in method:
            self.raw_data = extreme_obj.std_method(method['std']['sigma_multiple'])
        elif ExtremeMethod.MAD.value in method:
            self.raw_data = extreme_obj.mad_method(method['mad']['median_multiple'])
        elif ExtremeMethod.BOX_PLOT.value in method:
            self.raw_data = extreme_obj.std_method(method['std']['sigma_multiple'])
        else:
            raise Exception('This method is invalid!')

        return self.raw_data


class Extreme(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def data_replace(self, data_stock, raw_data_max, raw_data_min):
        data_stock[data_stock > raw_data_max] = raw_data_max
        data_stock[data_stock < raw_data_min] = raw_data_min
        return data_stock

    def std_method(self, sigma_multiple):
        raw_data_mean = self.raw_data.mean(axis=1)
        raw_data_std = self.raw_data.std(axis=1)
        raw_data_max = raw_data_mean + sigma_multiple * raw_data_std
        raw_data_min = raw_data_mean - sigma_multiple * raw_data_std
        return self.raw_data.apply(self.data_replace, args=(raw_data_max, raw_data_min))

    def mad_method(self, median_multiple):
        raw_data_median = self.raw_data.median(axis=1)
        raw_data_median_deviation = self.raw_data.sub(raw_data_median, axis=0)
        raw_data_mad = raw_data_median_deviation.median(axis=1)
        raw_data_max = raw_data_median + median_multiple * raw_data_mad
        raw_data_min = raw_data_median - median_multiple * raw_data_mad
        return self.raw_data.apply(self.data_replace, args=(raw_data_max, raw_data_min))

    def box_plot_method(self):
        pass


if __name__ == '__main__':
    indicator_data = SaveGetIndicator().get_indicator('ma5')
    factor_pre_obj = FactorPreProcessing(indicator_data)
    # extreme_data = factor_pre_obj.extreme_processing(dict(std={'sigma_multiple': 1}))
    extreme_data = factor_pre_obj.extreme_processing(dict(md={'median_multiple': 1}))
