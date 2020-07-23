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

from AmazingQuant.constant import DatabaseName
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from apps.server.database_server.database_field.field_multi_factor import FactorRegressionAnalysisResult


class FactorWeighting(object):
    def __init__(self, factor_return=None):
        # 因子收益率，单利，复利, 日收益率
        self.factor_return = factor_return

    def weighting_equal(self):
        result = None
        for i in self.factor_return:
            if result is None:
                result = self.factor_return[i]
            else:
                result += self.factor_return[i]
        return result / len(self.factor_return)

    def weighting_history_ir(self, window=20):
        result = None
        factor_ic_dict = {}
        for factor in self.factor_return:
            factor_ic_dict[factor] = self.factor_return[factor].rolling(window=window).mean() / \
                                     self.factor_return[factor].rolling(window=window).std()
            if result is None:
                result = factor_ic_dict[factor]
            else:
                result += factor_ic_dict[factor]
        return result / len(self.factor_return)


if __name__ == '__main__':
    factor_list = ['factor_ma5', 'factor_ma10']

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

    factor_weighting_obj = FactorWeighting(factor_return)
    factor_weighting_equal = factor_weighting_obj.weighting_equal()
    factor_history_ic = factor_weighting_obj.weighting_history_ir()
