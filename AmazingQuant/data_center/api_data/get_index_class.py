# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/27
# @Author  : gao
# @File    : get_index_class.py
# @Project : AmazingQuant
# ------------------------------
import pandas as pd
from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath


class GetIndexClass(object):
    def __init__(self):
        self.index_class_df = None

    def get_index_class(self):
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = LocalDataFolderName.SW_INDUSTRY_ONE.value + '.h5'
        self.index_class_df = pd.read_hdf(path + data_name)
        return self.index_class_df


if __name__ == '__main__':
    index_class_obj = GetIndexClass()
    index_class = index_class_obj.get_index_class()
