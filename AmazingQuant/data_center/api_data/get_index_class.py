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
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.utils.data_transfer import datetime_to_int


class GetIndexClass(object):
    def __init__(self):
        self.index_class_df = None
        self.zero_index_class = None
        self.code_list = []

    def get_index_class(self):
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = 'sw_industry_one' + '.h5'
        self.index_class_df = get_local_data(path, data_name)

        members_date = str(datetime_to_int(datetime.now()))
        self.index_class_df.loc[self.index_class_df.CON_OUTDATE.isna(), 'CON_OUTDATE'] = members_date
        self.index_class_df = self.index_class_df.reset_index(drop=True)
        self.code_list = self.index_class_df['CON_CODE'].unique()
        return self.index_class_df

    def get_zero_index_class(self):
        """
        初始化一个0的dataframe
        :return:
        """
        self.zero_index_class = pd.DataFrame(index=self.code_list,
                                             columns=sw_industry_one.keys()).fillna(0)

    def get_code_index_class_in_date(self, code, members_date):
        industry = 'other'
        if code in self.code_list:
            members_date = str(datetime_to_int(members_date))
            industry = self.index_class_df[(self.index_class_df.CON_INDATE <= members_date) &
                                           (self.index_class_df.CON_OUTDATE >= members_date) &
                                           (self.index_class_df.CON_CODE == code)]['INDEXNAME'].values[0]
        return industry

    def get_index_class_in_date(self, members_date):
        members_date = str(datetime_to_int(members_date))
        index_class_in_date = self.zero_index_class.copy()
        members_date_index_class = self.index_class_df[(self.index_class_df.CON_INDATE <= members_date) &
                                                       (self.index_class_df.CON_OUTDATE >= members_date)]
        print(members_date_index_class)
        members_date_index_class_grouped = members_date_index_class.groupby('INDEX_CODE')
        print(members_date_index_class_grouped.groups)

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
