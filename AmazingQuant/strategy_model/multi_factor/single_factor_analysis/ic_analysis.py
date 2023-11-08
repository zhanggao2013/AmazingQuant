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
1.method = {‘pearsonr’, ‘spearmanr’}，两种方法计算IC 和 rankIC
2.评价指标
    IC信号衰减计算,全部都计算时间序列
    （1） IC均值
    （2） IC标准差
    （3） IC_IR比率
    （4） IC>0占比
    （5） |IC|>0.02占比(绝对值)
    （6） p-value（有效性）
    （7） 偏度ic_skewness
    （8） 峰度ic_kurtosis

    （9） 正相关显著比例：显著的正相关系数占样本的比例
    （10）负相关显著比例：显著的负相关系数占样本的比例
    （11）状态切换比例：前后两期中相关系数符号相反占样本的比例。
    （12）同向比例：前后两期中相关系数符号相同占样本的比例。
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
# from apps.server.database_server.database_field.field_multi_factor import FactorIcAnalysisResult
# from AmazingQuant.constant import DatabaseName
# from AmazingQuant.utils.mongo_connection_me import MongoConnect


class IcAnalysis(object):
    def __init__(self, factor, factor_name, market_close_data):
        self.factor = factor
        self.factor_name = factor_name
        market_data = market_close_data.reindex(factor.index).reindex(factor.columns, axis=1)

        self.ic_decay = 20
        self.column_prefix = 'delay_'
        column_list = [self.column_prefix + str(i + 1) for i in range(self.ic_decay)]
        self.stock_return_dict = {i + 1: market_data.pct_change(periods=i + 1) for i in range(self.ic_decay)}

        # IC信号衰减计算，index 是时间序列， columns是decay周期，[1, self.ic_decay], 闭区间
        self.ic_df = pd.DataFrame(columns=column_list)

        self.p_value_df = pd.DataFrame(columns=column_list)

        # IC均值、 IC标准差、 IC_IR比率、 IC > 0 占比、 | IC | > 0.02 占比(绝对值)、 偏度、 峰度、
        # 正相关显著比例、负相关显著比例、状态切换比例、同向比例
        index_list = ['ic_mean', 'ic_std', 'ic_ir', 'ic_ratio', 'ic_abs_ratio', 'ic_skewness', 'ic_kurtosis',
                      'ic_positive_ratio', 'ic_negative_ratio', 'ic_change_ratio', 'ic_unchange_ratio', ]
        self.ic_result = pd.DataFrame(index=index_list, columns=column_list)

    def cal_ic_df(self, method='spearmanr'):
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
                    stock_return = self.stock_return_dict[ic_decay + 1].iloc[index].dropna()
                    factor_data = self.factor.iloc[index - ic_decay - 1].dropna()
                    stock_list = list(set(stock_return.index).intersection(set(factor_data.index)))
                    if method == 'spearmanr':
                        corr, p_value = stats.spearmanr(stock_return[stock_list].sort_index(),
                                                        factor_data[stock_list].sort_index())
                    elif method == 'pearsonr':
                        corr, p_value = stats.pearsonr(stock_return[stock_list].sort_index(),
                                                       factor_data[stock_list].sort_index())
                ic_dict[self.column_prefix + str(ic_decay + 1)] = corr
                p_value_dict[self.column_prefix + str(ic_decay + 1)] = p_value
            self.ic_df = pd.concat([self.ic_df, pd.DataFrame(ic_dict, index=[self.factor.index[index]])])
            self.p_value_df = pd.concat([self.p_value_df, pd.DataFrame(p_value_dict, index=[self.factor.index[index]])])
        return self.ic_df, self.p_value_df

    def cal_ic_indicator(self):
        self.ic_result.loc['ic_mean'] = self.ic_df.mean()
        self.ic_result.loc['ic_std'] = self.ic_df.std()
        self.ic_result.loc['ic_ir'] = self.ic_result.loc['ic_mean'] / self.ic_result.loc['ic_std']

        ic_count = self.ic_df.count()
        ic_greater_zero = self.ic_df > 0
        self.ic_result.loc['ic_ratio'] = self.ic_df[ic_greater_zero].count().div(ic_count)

        ic_abs = ic_analysis_obj.ic_df.abs()
        self.ic_result.loc['ic_abs_ratio'] = ic_abs[ic_abs > 0.02].count().div(ic_count)

        self.ic_result.loc['ic_skewness'] = self.ic_df.skew()
        self.ic_result.loc['ic_kurtosis'] = self.ic_df.kurt()

        p_value_significant = self.p_value_df[self.p_value_df < 0.05].count()
        self.ic_result.loc['ic_positive_ratio'] = p_value_significant.div(ic_count) * 100
        self.ic_result.loc['ic_negative_ratio'] = (ic_count - p_value_significant).div(ic_count) * 100

        change_df = ic_greater_zero.iloc[:-1].values != ic_greater_zero.iloc[1:].values
        ic_change_num = pd.DataFrame(change_df, columns=self.ic_df.columns).sum()

        self.ic_result.loc['ic_change_ratio'] = ic_change_num.div(ic_count) * 100
        self.ic_result.loc['ic_unchange_ratio'] = (ic_count - ic_change_num).div(ic_count) * 100

    def save_ic_analysis_result(self, factor_name):
    #     with MongoConnect(DatabaseName.MULTI_FACTOR_DATA.value):
    #         ic_df = self.ic_df.copy()
    #         p_value_df = self.p_value_df.copy()
    #         ic_df.index = ic_df.index.format()
    #         p_value_df.index = p_value_df.index.format()
    #         doc = FactorIcAnalysisResult(
    #             factor_name=factor_name,
    #             # 因子数据开始时间
    #             begin_date=self.factor.index[0],
    #             # 因子数据结束时间
    #             end_date=self.factor.index[-1],
    #             # IC信号衰减计算，index 是时间序列， columns是decay周期，[1, self.ic_decay], 闭区间
    #             ic=ic_df,
    #             # p值信号衰减计算，index 是时间序列， columns是decay周期，[1, self.ic_decay], 闭区间
    #             p_value=p_value_df,
    #             # IC均值、 IC标准差、 IC_IR比率、 IC > 0 占比、 | IC | > 0.02 占比(绝对值)、 偏度、 峰度、
    #             # 正相关显著比例、负相关显著比例、状态切换比例、同向比例
    #             # index_list=['ic_mean', 'ic_std', 'ic_ir', 'ic_ratio', 'ic_abs_ratio', 'ic_skewness', 'ic_kurtosis',
    #             #             'ic_positive_ratio', 'ic_negative_ratio', 'ic_change_ratio', 'ic_unchange_ratio', ]
    #             ic_result=self.ic_result)
    #         doc.save()




if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_name = 'factor_ma5'
    factor_ma5 = get_local_data(path, factor_name + '.h5')
    factor_ma5 = factor_ma5.iloc[:200, :]
    import datetime
    factor_ma5 = factor_ma5[factor_ma5.index < datetime.datetime(2016, 1, 1)]

    market_close_data = GetKlineData().cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value,
                                                            field=['close'])['close']
    ic_analysis_obj = IcAnalysis(factor_ma5, factor_name, market_close_data)
    ic_analysis_obj.cal_ic_df(method='spearmanr')
    ic_analysis_obj.cal_ic_indicator()
    # ic_analysis_obj.save_ic_analysis_result(factor_name)

