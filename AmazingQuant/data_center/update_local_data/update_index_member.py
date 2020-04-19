# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/13
# @Author  : gao
# @File    : update_index_member.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd

from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from apps.server.database_field.field_a_share_index_members import AShareIndexMembers
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.mongo_connection_me import MongoConnect


class UpdateIndexMember(object):
    def __init__(self):
        self.index_members_df = pd.DataFrame.empty
        self.index_members_all = []

    def update_index_members(self):
        database = DatabaseName.STOCK_BASE_DATA.value
        with MongoConnect(database):
            index_members_data = AShareIndexMembers.objects().as_pymongo()
            field_list = ['index_code', 'security_code', 'in_date', 'out_date']
            self.index_members_df = pd.DataFrame(list(index_members_data)).reindex(columns=field_list)
            folder_name = LocalDataFolderName.INDEX_MEMBER.value
            path = LocalDataPath.path + folder_name + '/'
            data_name = folder_name
            save_data_to_hdf5(path, data_name, self.index_members_df)


if __name__ == '__main__':
    index_member_obj = UpdateIndexMember()
    index_member_obj.update_index_members()


