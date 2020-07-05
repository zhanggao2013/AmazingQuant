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
from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class CollinearityAnalysis(object):
    def __init__(self, factor_data=None):
        """
        :param factor_data: dict, key(str):factor name, value(dataframe):factor data
        """
        self.factor_data = factor_data

    def cal_data_relation(self):
        """

        :return: Dataframe, multiindex: time_tag -- factor name, columns: factor name
        """
        pass

    def cal_vif(self):
        """

        :return:Dataframe, index: time_tag , columns: factor name
        """
        pass

    def cal_condition_num(self):
        """

        :return: Series, index: time_tag
        """
        pass


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
