# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/30
# @Author  : gao
# @File    : get_index_member.py
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime

import pandas as pd

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.utils.data_transfer import datetime_to_int


class GetIndexMember(object):
    def __init__(self):
        self.all_index_members_df = pd.DataFrame.empty
        self.index_members_df = pd.DataFrame.empty
        self.industry_members_df = pd.DataFrame.empty
        self.index_members_all = []

    def get_all_index_members(self):
        folder_name = LocalDataFolderName.INDEX_MEMBER.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = folder_name + '.h5'
        self.all_index_members_df = get_local_data(path, data_name)

        members_date = str(datetime_to_int(datetime.now()))
        self.all_index_members_df.loc[self.all_index_members_df.CON_OUTDATE.isna(), 'CON_OUTDATE'] = members_date
        self.all_index_members_df = self.all_index_members_df.reset_index(drop=True)
        return self.all_index_members_df

    def get_index_members(self, index_code):
        index_members_df = self.all_index_members_df[(self.all_index_members_df.INDEX_CODE == index_code)]
        index_members_all = list(set(index_members_df['CON_CODE']))
        return index_members_all

    def get_index_member_in_date(self, members_date=datetime.now(), index_code=''):
        """
        取指定日期的指数成分股
        :param members_date:
        :return:
        """
        members_date = str(datetime_to_int(members_date))
        index_members_in_date_df = self.all_index_members_df[(self.all_index_members_df.CON_INDATE <= members_date) &
                                                             (self.all_index_members_df.CON_OUTDATE >= members_date)]
        if index_code:
            index_members_in_date_df = index_members_in_date_df[(index_members_in_date_df.INDEX_CODE == index_code)]
        index_members_in_date_list = list(set(index_members_in_date_df['CON_CODE']))
        return index_members_in_date_list


if __name__ == '__main__':
    index_member_obj = GetIndexMember()
    all_index_members_df = index_member_obj.get_all_index_members()
    # 深证综指
    index_members_all_SZ = index_member_obj.get_index_members(index_code='399106.SZ')
    # 上证Ａ股
    index_members_all_SH = index_member_obj.get_index_members(index_code='000001.SH')
    # 沪深300
    index_member_in_date = index_member_obj.get_index_member_in_date(index_code='000300.SH')
