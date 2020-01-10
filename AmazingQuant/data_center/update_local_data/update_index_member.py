# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/13
# @Author  : gao
# @File    : update_index_member.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

import pandas as pd
from mongoengine import connection

from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.database_info import MongodbConfig
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.database_field.field_a_share_index_members import AShareIndexMembers
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5


class UpdateGIndexMember(object):
    def __init__(self):
        self.index_members_df = pd.DataFrame.empty
        self.index_members_all = []

    def update_index_members(self):
        database = DatabaseName.STOCK_BASE_DATA.value
        connection.connect(db=database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        index_members_data = AShareIndexMembers.objects().as_pymongo()
        connection.disconnect()

        field_list = ['index_code', 'security_code', 'in_date', 'out_date']
        self.index_members_df = pd.DataFrame(list(index_members_data)).reindex(columns=field_list)
        print(self.index_members_df)
        folder_name = LocalDataFolderName.INDEX_MEMBER.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = folder_name
        save_data_to_hdf5(path, data_name, self.index_members_df)


if __name__ == '__main__':
    index_member_obj = UpdateGIndexMember()
    index_member_obj.update_index_members()


