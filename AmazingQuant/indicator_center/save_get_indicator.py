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
        pass

    def save_indicator(self, indicator_name, input_data):
        path_save = LocalDataPath.path + 'indicator/'
        if not os.path.exists(path_save):
            os.mkdir(path_save)
        input_data.to_hdf(path_save + indicator_name + '.h5', key=indicator_name, mode='w')

    def get_indicator(self, indicator_name):
        data_path = LocalDataPath.path + 'indicator/' + indicator_name + '.h5'
        if not os.path.exists(data_path):
            return None
        return pd.read_hdf(data_path)


if __name__ == '__main__':
    with Timer(True):
        indicator_data = SaveGetIndicator().get_indicator('ma5')

