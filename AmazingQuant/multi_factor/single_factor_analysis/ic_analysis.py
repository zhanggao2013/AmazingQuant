# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : ic_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
IC分析
IC是指因子在第T期的因子值与T+1期的股票收益的相关系数
1.计算rank_IC
2.评价指标
    （1） IC均值
    （2） IC标准差
    （3） IC_IR比率
    （4） IC>0占比
    （5） |IC|>0.02占比(绝对值)
    （6） p-value（有效性）,全部都计算时间序列
    （7） IC信号衰减计算
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.data_center.api_data.get_kline import GetKlineData


class IcAnalysis(object):
    def __init__(self, factor):
        self.factor = factor
        market_data = \
            GetKlineData().cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value, field=['close'])['close']
        self.stock_return = market_data.pct_change().reindex(factor.index).reindex(factor.columns, axis=1)
        self.ic_series = pd.Series({self.factor.index[0]: np.nan})
        self.p_value_series = pd.Series({self.factor.index[0]: np.nan})

    def cal_ic_series(self, method='spearmanr'):
        """
        method = {‘pearsonr’, ‘spearmanr’}
        :param method:
        :return:
        """
        index_num = 0
        for index, data in self.stock_return.iterrows():
            if index_num >= 1:
                stock_list = list(set(data.dropna().index).
                                  intersection(set(self.factor.iloc[index_num - 1].dropna().index))
                                  )
                corr = np.nan
                p_value = np.nan
                if method == 'spearmanr':
                    corr, p_value = stats.spearmanr(data[stock_list], self.factor.iloc[index_num - 1][stock_list])
                elif method == 'pearsonr':
                    corr, p_value = stats.pearsonr(data[stock_list], self.factor.iloc[index_num - 1][stock_list])
                self.ic_series[index] = corr
                self.p_value_series[index] = p_value
            index_num += 1
        return self.ic_series


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')

    ic_analysis_obj = IcAnalysis(factor_ma5)
    ic_series = ic_analysis_obj.cal_ic_series(method='spearmanr')
