# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : stratification_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
分层法
1 各种净值的指标计算方法
2 换手率分析
（1）个数法换手率分析
    所谓个数法就是计算每期之间股票变动的数量并除以股票的总数量计算出的比率，例如t期买入[A,B,C,D,E]五只股票，t+1期买入[A,D,E,F,G]五只股票，那么这期间的换手率就是(2/5=40%)。
（2）权重法换手率分析
    权重法不仅考虑股票本身的变化，还考虑了股票权重的变化。
（3）买入信号衰减与反转
3 板块分析
（1）group_cap_mean：每组选出股票的市值均值
（2）group_industry_ratio:每组所有行业占比的时间序列
（3）group_industry_mean_ratio：每组所有时间的行业平均占比,就是（2）时间序列上求平均
（4）group_stock_list：每组选出股票的代码,
（5）plot_industry_ratio():每组行业占比热力图
"""
import datetime

import numpy as np
import pandas as pd

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class StratificationAnalysis(object):
    def __init__(self, factor, factor_name):
        self.factor = factor
        self.factor_name = factor_name

    def add_group(self, group_num, ascending=True):
        factor_ma5_rank = self.factor.rank(axis=1, ascending=ascending)
        group_key = ['group_' + str(i) for i in range(group_num)]
        return factor_ma5_rank.apply(lambda x: pd.cut(x, group_num, labels=group_key), axis=1)


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma5 = factor_ma5[factor_ma5.index < datetime.datetime(2020, 1, 1)]
    stratification_analysis_obj = StratificationAnalysis(factor_ma5, 'factor_ma5')
    factor_ma5_rank = stratification_analysis_obj.add_group(5)

