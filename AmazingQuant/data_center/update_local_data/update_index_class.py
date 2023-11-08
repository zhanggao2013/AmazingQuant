# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/26
# @Author  : gao
# @File    : update_index_class.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd
from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from apps.server.database_server.database_field.field_a_share_index_members import AShareIndexMembers
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.data_center.api_data.get_collection_list import GetCollectionList
from AmazingQuant.data_center.api_data.get_calender import GetCalendar
from AmazingQuant.config.industry_class import sw_industry_one


class UpdateIndexMember(object):
    def __init__(self):
        self.database = DatabaseName.STOCK_BASE_DATA.value
        self.index_members_df = pd.DataFrame.empty
        self.index_class = None

    def update_index_class(self, industry_class_name, industry_class_dict):
        with MongoConnect(self.database):
            index_members_data = AShareIndexMembers.objects(index_code__in=industry_class_dict.keys()).as_pymongo()
            field_list = ['index_code', 'security_code', 'in_date', 'out_date']
            self.index_members_df = pd.DataFrame(list(index_members_data)).reindex(columns=field_list)
            self.index_members_df = self.index_members_df.fillna(datetime.now()).reset_index(drop=True)

            get_collection_list = GetCollectionList()
            a_share_list = get_collection_list.get_a_share_list()
            calendar_obj = GetCalendar()
            calendar_SH = calendar_obj.get_calendar('SH')
            self.index_class = pd.DataFrame(columns=a_share_list, index=calendar_SH)

            def industry_history(x, index_members_df):
                industry_in_out_date = index_members_df[index_members_df.security_code == x.name]
                for index, row in industry_in_out_date.iterrows():
                    x[row['in_date']: row['out_date']] = row['index_code']
                return x

            self.index_class = self.index_class.apply(industry_history, args=(self.index_members_df,), axis=0)
            self.index_class = self.index_class.fillna(method='pad').fillna(method='backfill')
            folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
            path = LocalDataPath.path + folder_name + '/'
            data_name = industry_class_name
            save_data_to_hdf5(path, data_name, self.index_class)


if __name__ == '__main__':
    index_member_obj = UpdateIndexMember()
    index_member_obj.update_index_class('sw_industry_one', sw_industry_one)
