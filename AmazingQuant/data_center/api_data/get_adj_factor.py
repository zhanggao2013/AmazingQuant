# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/1/10
# @Author  : gao
# @File    : get_adj_factor.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment, AdjustmentFactor
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.performance_test import Timer


class GetAdjFactor(object):
    def __init__(self):
        pass

    def get_adj_factor(self, adjustment_mode):
        folder_name = LocalDataFolderName.ADJ_FACTOR.value
        path = LocalDataPath.path + folder_name + '/'
        data = pd.DataFrame({})
        if adjustment_mode == RightsAdjustment.BACKWARD.value:
            data = pd.read_hdf(path + AdjustmentFactor.BACKWARD_ADJ_FACTOR.value + '.h5')
        elif adjustment_mode == RightsAdjustment.FROWARD.value:
            data = pd.read_hdf(path + AdjustmentFactor.FROWARD_ADJ_FACTOR.value + '.h5')
        return data


if __name__ == '__main__':
    with Timer(True):
        adj_factor_obj = GetAdjFactor()
        result = adj_factor_obj.get_adj_factor(RightsAdjustment.FROWARD.value)

