# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : collinearity_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
因子共线性分析
(1)相关性分析
(2)方差膨胀因子VIF
(3)条件数
"""
from datetime import datetime

import pandas as pd
import statsmodels.api as sm
import numpy as np

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class CollinearityAnalysis(object):
    def __init__(self, factor_data=None):
        """
        :param factor_data: Dataframe, multiindex: factor name--time_tag, columns: stock code
        """
        self.factor_data = pd.concat(factor_data, names=['factor_name'])
        self.time_tag_index = self.factor_data.index.levels[1].unique()
        self.factor_name_index = self.factor_data.index.levels[0].unique()
        # 相关系数， Dataframe, multiindex: time_tag -- factor name, columns: factor name
        self.relation = None
        # 方差膨胀因子vif, Dataframe, index: time_tag , columns: factor name
        self.vif = pd.DataFrame(columns=self.factor_data.index.levels[0].unique())
        # 条件数, Series, index: time_tag
        self.condition_num = pd.Series(index=self.time_tag_index)

    def cal_relation(self, time_tag, time_tag_data):
        if time_tag == self.time_tag_index[0]:
            self.relation = {}
        self.relation[time_tag] = time_tag_data.T.corr()
        if time_tag == self.time_tag_index[-1]:
            self.relation = pd.concat(self.relation, names=['time_tag'])

    def cal_vif(self, time_tag, time_tag_data):
        vif_dict = {}
        for factor_name in self.factor_name_index:
            model = sm.OLS(time_tag_data.loc[factor_name].T,
                           sm.add_constant(time_tag_data[time_tag_data.index != factor_name].T))
            r_squared = model.fit().rsquared
            if r_squared < 1:
                vif_dict[factor_name] = 1 / (1 - r_squared)
            else:
                vif_dict[factor_name] = np.nan
        self.vif = self.vif.append(pd.Series(vif_dict, name=time_tag))

    def cal_condition_num(self, time_tag, time_tag_data):
        self.condition_num[time_tag] = np.linalg.cond(time_tag_data.T.values)

    def cal_collinearity(self):
        for time_tag in self.time_tag_index:
            time_tag_data = self.factor_data[self.factor_data.index.get_level_values(1) == time_tag]
            time_tag_data = time_tag_data.reset_index(level='time_tag', drop=True)
            self.cal_relation(time_tag, time_tag_data)
            self.cal_vif(time_tag, time_tag_data)
            self.cal_condition_num(time_tag, time_tag_data)


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma5 = factor_ma5[factor_ma5.index < datetime(2020, 1, 1)]
    factor_ma10 = get_local_data(path, 'factor_ma10.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma10 = factor_ma10[factor_ma10.index < datetime(2020, 1, 1)]
    factor_data = {'factor_ma5': factor_ma5, 'factor_ma10': factor_ma10}

    collinearity_analysis_obj = CollinearityAnalysis(factor_data)
    collinearity_analysis_obj.cal_collinearity()

