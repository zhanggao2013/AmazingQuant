# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : save_get_indicator.py
# @Project : AmazingQuant 
# ------------------------------
import os

import pandas as pd

from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.config.local_data_path import LocalDataPath


class SaveGetIndicator(object):
    def __init__(self):
        self.path_save = LocalDataPath.path + 'indicator/'

    def save_indicator(self, indicator_name, input_data):
        if not os.path.exists(self.path_save):
            os.mkdir(self.path_save)
        input_data.to_hdf(self.path_save + indicator_name + '.h5', key=indicator_name, mode='w')

    def get_indicator(self, indicator_name):
        data_path = self.path_save + indicator_name + '.h5'
        if not os.path.exists(data_path):
            return None
        return pd.read_hdf(data_path)


if __name__ == '__main__':
    with Timer(True):
        indicator_data = SaveGetIndicator().get_indicator('ma5')

