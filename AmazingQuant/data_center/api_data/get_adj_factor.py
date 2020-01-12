# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/1/10
# @Author  : gao
# @File    : get_adj_factor.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from AmazingQuant.constant import LocalDataFolderName, AdjustmentMode
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.performance_test import Timer


class GetAdjFactor(object):
    def __init__(self):
        pass

    def get_adj_factor(self, adjustment_mode):
        folder_name = LocalDataFolderName.ADJ_FACTOR.value
        path = LocalDataPath.path + folder_name + '/'
        data = pd.DataFrame({})
        if adjustment_mode == AdjustmentMode.RIGHT.value:
            data_name = folder_name + '_' + adjustment_mode + '.h5'
            data = pd.read_hdf(path + data_name)
        elif adjustment_mode == AdjustmentMode.RIGHT.value:
            data_name = folder_name + '_' + adjustment_mode + '.h5'
            data = pd.read_hdf(path + data_name)
        return data

if __name__ == '__main__':
    from AmazingQuant.data_center.api_data.get_calender import GetCalendar
    with Timer(True):
        adj_factor_obj = GetAdjFactor()
        result = adj_factor_obj.get_adj_factor(AdjustmentMode.RIGHT.value)
        # result_a = {}
        # for i in result:
        #     result[i].set_index(["ex_date"], inplace=True)
        # print(result)
"""
存成与日线数据相同格式的hdf5文件，取出来直接与open   close相乘
"""
