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

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class FactorWeighting(object):
    def __init__(self, factor_data=None):
        self.factor_data = factor_data
        # 因子收益率，单利，复利
        self.factor_return = pd.DataFrame(index=self.factor_data.values()[0].index, columns=['cumsum', 'cumprod'])
        self.factor_return_daily = None

    def weighting_equal(self):
        result = None
        for i in self.factor_data:
            if result is None:
                result = self.factor_data[i]
            else:
                result += self.factor_data[i]
        return result


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma5 = factor_ma5[factor_ma5.index < datetime(2020, 1, 1)]
    factor_ma10 = get_local_data(path, 'factor_ma10.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma10 = factor_ma10[factor_ma10.index < datetime(2020, 1, 1)]
    factor_data = {'factor_ma5': factor_ma5, 'factor_ma10': factor_ma10}
    factor_weighting_obj = FactorWeighting(factor_data)
    factor_weighting_equal = factor_weighting_obj.weighting_equal()