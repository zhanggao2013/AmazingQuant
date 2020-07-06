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
    行业中性时,如果没有所属行业,则行业中性化后为nan

4.标准化
    (1) 最小-最大值差标准化
    (2) Z-score标准化,
    (3) 排序百分位,标准化成均匀分布

5.补空值
    个股所处行业均值（未实现）
    所有股票的均值
    中位数

"""
import math
from datetime import datetime

import pandas as pd
import numpy as np
import statsmodels.api as sm

from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.strategy_model.multi_factor.multi_factor_constant import ExtremeMethod, ScaleMethod, FillNanMethod,\
    NeutralizeMethod
from AmazingQuant.data_center.api_data.get_index_class import GetIndexClass
from AmazingQuant.data_center.api_data.get_share import GetShare
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath


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

    def fill_nan_processing(self, method=None):
        if method is None:
            method = FillNanMethod.MEAN.value
        fill_nan_obj = FillNan(self.raw_data)
        if FillNanMethod.MEAN.value in method:
            self.raw_data = fill_nan_obj.mean_method()
        elif FillNanMethod.MID.value in method:
            self.raw_data = fill_nan_obj.median_method()
        return self.raw_data

    def neutralize_processing(self, method=None):
        if method is None:
            method = dict(neutralize_method=NeutralizeMethod.INDUSTRY.value)
        neutralize_obj = Neutralize(self.raw_data)
        if NeutralizeMethod.INDUSTRY.value in method['neutralize_method']\
                or NeutralizeMethod.MARKET_VALUE.value in method['neutralize_method']:
            self.raw_data = neutralize_obj.neutralize_method(method['neutralize_method'])
        else:
            raise Exception('This extreme method is invalid!')
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
        raw_data_median_deviation = self.raw_data.sub(raw_data_median, axis=0).abs()
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


class FillNan(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def mean_method(self):
        raw_data_mean = self.raw_data.mean(axis=1)
        return self.raw_data.T.fillna(raw_data_mean).T

    def median_method(self):
        raw_data_median = self.raw_data.median(axis=1)
        return self.raw_data.T.fillna(raw_data_median).T


class Neutralize(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def neutralize_method(self, method):
        index_class_obj = GetIndexClass()
        index_class_obj.get_index_class()
        index_class_obj.get_zero_index_class()

        share_data = pd.DataFrame({})
        if NeutralizeMethod.MARKET_VALUE.value in method:
            share_data_obj = GetShare()
            share_data = share_data_obj.get_share('float_a_share_value')

        def cal_resid(data, index_class_obj, share_data, method):
            # 删除一些 , 因子数据为NAN的个股
            data = data.dropna()
            index_class_in_date = pd.DataFrame({})
            share_data_in_date = pd.DataFrame({})

            if NeutralizeMethod.INDUSTRY.value in method:
                index_class_in_date = index_class_obj.get_index_class_in_date(data.name)
            if NeutralizeMethod.MARKET_VALUE.value in method:
                share_data_in_date = share_data.loc[data.name].dropna()
                share_data_in_date = pd.DataFrame({'float_a_share_value': share_data_in_date})

            # 行业中性与流通市值中性化取交集
            neutralize_data = index_class_in_date.join(share_data_in_date, how='outer').dropna()
            # 因子数据的股票list与中性化数据的股票list,取交集
            stock_code_list = list(set(data.index).intersection(set(neutralize_data.index)))
            # 因子数据取 有效股票列表数据，并排序
            factor = data[stock_code_list].sort_index()
            # 中性化数据取 有效股票列表数据，并排序
            neutralize_data = neutralize_data.reindex(stock_code_list).sort_index()

            # 回归
            neutralize_data = sm.add_constant(neutralize_data)
            model = sm.OLS(factor, neutralize_data)
            fit_result = model.fit()
            # 残差作为中性化后的数据
            return fit_result.resid

        self.raw_data = self.raw_data.apply(cal_resid, args=(index_class_obj, share_data, method,), axis=1)
        return self.raw_data


if __name__ == '__main__':
    indicator_data = SaveGetIndicator().get_indicator('ma10')

    factor_pre_obj = FactorPreProcessing(indicator_data)
    # 可根据时间和股票list过滤数据
    data_filter = factor_pre_obj.data_filter()
    # 去极值方法，四种
    extreme_data = factor_pre_obj.extreme_processing(dict(std={'sigma_multiple': 3}))
    # extreme_data = factor_pre_obj.extreme_processing(dict(mad={'median_multiple': 1.483}))
    # extreme_data = factor_pre_obj.extreme_processing(dict(quantile={'quantile_min': 0.025, 'quantile_max': 0.975}))
    # extreme_data = factor_pre_obj.extreme_processing(dict(box_plot={'median_multiple': 3}))

    # 中性化方法，可选择行业和流通市值中性
    neutralize_data = factor_pre_obj.neutralize_processing(dict(neutralize_method=[NeutralizeMethod.INDUSTRY.value, NeutralizeMethod.MARKET_VALUE.value]))

    # 归一化方法，三种
    # scale_data = factor_pre_obj.scale_processing(ScaleMethod.MIN_MAX.value)
    scale_data = factor_pre_obj.scale_processing(ScaleMethod.Z_SCORE.value)
    # scale_data = factor_pre_obj.scale_processing(ScaleMethod.RANK.value)

    # 补充空值的方法，已实现两种
    fill_nan_data = factor_pre_obj.fill_nan_processing(FillNanMethod.MEAN.value)

    # 保存预处理之后的因子数据，单因子检测使用
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    save_data_to_hdf5(path, 'factor_ma10', fill_nan_data)



