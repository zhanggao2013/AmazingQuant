# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : factor_weighting.py
# @Project : AmazingQuant
# ------------------------------
"""
因子加权方法
(1)等权法
(2)历史信息比例(IR)加权法
(3)历史收益率加权法,均值和半衰
(4)历史IC加权法,均值和半衰
(5)最大化IC_IR加权法
(6)最大化IC加权法
"""
from datetime import datetime

import pandas as pd
import numpy as np

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.constant import DatabaseName
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from apps.server.database_server.database_field.field_multi_factor import FactorRegressionAnalysisResult


class FactorWeighting(object):
    def __init__(self, factor_data, factor_return=None):
        # 因子数据
        self.factor_data = factor_data
        # 因子加权后的结果
        self.factor_data_weighted = None

    def weighting_history_return(self, factor_return, weight_method='equal', window=20):
        """
        :param factor_return:
        :param weight_method:'equal'，等权法，不需要window,
                              'return_mean'， 历史收益率加权法，平均值，window是平均值周期,
                              'return_half_life'，历史收益率加权法，半衰期法，window是半衰期,
                               'return_ir'，  历史因子收益率信息比例(IR)加权法，window是平均值周期

        :param window:
        :return:
        """

        factor_single_weight_dict = {}
        factor_total_weight = None
        for factor in factor_return:
            factor_single_weight_dict[factor] = None
            if weight_method == 'equal':
                factor_single_weight_dict[factor] = 1
            elif weight_method == 'return_mean':
                factor_single_weight_dict[factor] = factor_return[factor]['daily'].rolling(window=window).mean()
            elif weight_method == 'return_half_life':
                factor_single_weight_dict[factor] = factor_return[factor]['daily'].ewm(halflife=window).mean()
            elif weight_method == 'return_ir':
                factor_single_weight_dict[factor] = factor_return[factor]['daily'].rolling(window=window).mean() / \
                                                    factor_return[factor]['daily'].rolling(window=window).std()
            else:
                raise Exception('weight_method is not exist')

            if factor_total_weight is None:
                factor_total_weight = factor_single_weight_dict[factor]
            else:
                factor_total_weight = factor_total_weight + factor_single_weight_dict[factor]

        for factor in self.factor_data:
            factor_single_data_weighted = self.factor_data[factor].mul(
                factor_single_weight_dict[factor] / factor_total_weight, axis=0)
            if self.factor_data_weighted is None:
                self.factor_data_weighted = factor_single_data_weighted
            else:
                self.factor_data_weighted = self.factor_data_weighted + factor_single_data_weighted
        return self.factor_data_weighted


if __name__ == '__main__':
    factor_list = ['factor_ma5', 'factor_ma10']

    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_data = {}
    for factor_name in factor_list:
        factor_single_data = get_local_data(path, factor_name + '.h5')
        # 指数数据不全，需要删一部分因子数据
        factor_data[factor_name] = factor_single_data[factor_single_data.index < datetime(2020, 1, 1)]

    with MongoConnect(DatabaseName.MULTI_FACTOR_DATA.value):
        factor_return = {}
        for factor_name in factor_list:
            factor_regression_analysis_result = FactorRegressionAnalysisResult.objects(factor_name=factor_name) \
                .only('factor_name') \
                .only('begin_date') \
                .only('end_date') \
                .only('factor_return') \
                .as_pymongo()
            factor_return[factor_name] = pd.DataFrame(factor_regression_analysis_result[0]['factor_return'])
            factor_return[factor_name].index = pd.DatetimeIndex(factor_return[factor_name].index)

    factor_weighting_obj = FactorWeighting(factor_data)
    factor_history_return = factor_weighting_obj.weighting_history_return(factor_return, weight_method='equal')
