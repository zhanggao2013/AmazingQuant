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
    （6） p-value（有效性）
    （7） IC信号衰减计算,全部都计算时间序列
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.data_center.api_data.get_kline import GetKlineData


class IcAnalysis(object):
    def __init__(self, factor, factor_name):
        self.factor = factor
        self.factor_name = factor_name
        market_data = GetKlineData() \
            .cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value, field=['close'])['close'] \
            .reindex(factor.index) \
            .reindex(factor.columns, axis=1)

        self.ic_decay = 2
        self.stock_return_dict = {i + 1: market_data.pct_change(periods=i + 1) for i in range(self.ic_decay)}

        self.ic_df = pd.DataFrame(columns=[factor_name + '_' + str(i + 1) for i in range(self.ic_decay)])
        self.p_value_df = pd.DataFrame(columns=[factor_name + '_' + str(i + 1) for i in range(self.ic_decay)])

        self.ic_mean = None
        self.ic_std = None
        self.ic_ir = None
        self.ic_ratio = None
        self.ic_abs_ratio = None

    def cal_ic_series(self, method='spearmanr'):
        """
        method = {‘pearsonr’, ‘spearmanr’}
        :param method:
        :return:
        """
        for index in range(self.factor.shape[0]):
            print(self.factor.index[index])
            ic_dict = {}
            p_value_dict = {}
            for ic_decay in range(self.ic_decay):
                corr = np.nan
                p_value = np.nan
                if index > ic_decay:
                    stock_return = self.stock_return_dict[ic_decay+1].iloc[index].dropna()
                    factor_data = self.factor.iloc[index - ic_decay - 1].dropna()
                    stock_list = list(set(stock_return.index).intersection(set(factor_data.index)))
                    if method == 'spearmanr':
                        corr, p_value = stats.spearmanr(stock_return[stock_list], factor_data[stock_list])
                    elif method == 'pearsonr':
                        corr, p_value = stats.pearsonr(stock_return[stock_list], factor_data[stock_list])
                ic_dict[self.factor_name + '_' + str(ic_decay + 1)] = corr
                p_value_dict[self.factor_name + '_' + str(ic_decay + 1)] = p_value

            self.ic_df = self.ic_df.append(pd.Series(ic_dict, name=self.factor.index[index]))
            self.p_value_df = self.p_value_df.append(pd.Series(p_value_dict, name=self.factor.index[index]))
        return self.ic_df, self.p_value_df

    def cal_ic_indicator(self):
        self.ic_mean = self.ic_df.mean


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')

    ic_analysis_obj = IcAnalysis(factor_ma5, 'factor_ma5')
    ic_analysis_obj.cal_ic_series(method='spearmanr')
    ic_analysis_obj.cal_ic_indicator()
