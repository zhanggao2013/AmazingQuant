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
        self.all_index_members_df = pd.read_hdf(path + data_name)
        return self.all_index_members_df

    def get_index_members(self, index_code):
        self.index_members_df = self.all_index_members_df[self.all_index_members_df.index_code == index_code]
        self.index_members_df = self.index_members_df.fillna(datetime.now()).reset_index(drop=True)
        self.index_members_all = list(set(self.index_members_df['security_code']))
        return self.index_members_df, self.index_members_all

    def get_index_member_in_date(self, members_date=datetime.now()):
        """
        取指定日期的指数成分股
        :param members_date:
        :return:
        """
        index_members_in_date_df = self.index_members_df[
            (self.index_members_df.in_date <= members_date) & (self.index_members_df.out_date >= members_date)]
        return list(index_members_in_date_df["security_code"])


if __name__ == '__main__':
    index_member_obj = GetIndexMember()
    all_index_members_df = index_member_obj.get_all_index_members()
    # 深证综指
    index_members_df_SZ, index_members_all_SZ = index_member_obj.get_index_members('399106.SZ')
    # 上证Ａ股
    index_members_df_SH, index_members_all_SH = index_member_obj.get_index_members('000001.SH')
    # 申万行业指数--化工
    index_members_df_SI, index_members_all_SI = index_member_obj.get_index_members('801030.SI')

    index_member_in_date = index_member_obj.get_index_member_in_date()


