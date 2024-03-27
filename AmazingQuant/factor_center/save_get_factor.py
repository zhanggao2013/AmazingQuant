# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : save_get_factor.py
# @Project : AmazingQuant 
# ------------------------------
import os

import pandas as pd

from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.constant import LocalDataFolderName


class SaveGetFactor(object):
    def __init__(self):
        self.path_save = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'

    def save_factor(self, factor_name, input_data):
        save_data_to_hdf5(self.path_save + factor_name + '/', factor_name, input_data)

    def get_factor(self, factor_name):
        data_path = self.path_save + factor_name + '/'+ factor_name + '.h5'
        if not os.path.exists(data_path):
            return None
        return pd.read_hdf(data_path)


if __name__ == '__main__':
    with Timer(True):
        indicator_data = SaveGetFactor().get_factor('ma5')

