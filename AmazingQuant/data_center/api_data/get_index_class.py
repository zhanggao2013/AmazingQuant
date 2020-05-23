# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/27
# @Author  : gao
# @File    : get_index_class.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime

import pandas as pd
import numpy as np

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.config.industry_class import sw_industry_one


class GetIndexClass(object):
    def __init__(self):
        self.index_class_df = None
        self.zero_index_class = None

    def get_index_class(self):
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = LocalDataFolderName.SW_INDUSTRY_ONE.value + '.h5'
        self.index_class_df = pd.read_hdf(path + data_name)
        return self.index_class_df

    def get_zero_index_class(self):
        """
        初始化一个0的dataframe
        :return:
        """
        self.zero_index_class = pd.DataFrame(index=self.index_class_df.columns, columns=sw_industry_one.keys()).fillna(0)

    def get_index_class_in_date(self, members_date):
        index_class_in_date = self.zero_index_class.copy()
        members_date_index_class = self.index_class_df.loc[members_date]
        members_date_index_class_grouped = members_date_index_class.groupby(members_date_index_class)

        def cal_class(x, members_date_index_class_groups):
            if x.name in members_date_index_class_groups:
                x[members_date_index_class_groups[x.name]] = 1
            return x

        return index_class_in_date.apply(lambda x: cal_class(x, members_date_index_class_grouped.groups))


if __name__ == '__main__':
    index_class_obj = GetIndexClass()
    index_class = index_class_obj.get_index_class()
    index_class_obj.get_zero_index_class()

    index_class_in_date = index_class_obj.get_index_class_in_date(datetime(2020, 12, 31))

