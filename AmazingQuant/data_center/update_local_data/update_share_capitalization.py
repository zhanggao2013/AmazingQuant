# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/23
# @Author  : gao
# @File    : update_share_capitalization.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd

from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from apps.server.database_server.database_field.field_a_share_capitalization import AShareCapitalization
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.utils.mongo_connection_me import MongoConnect


class UpAShareCapitalization(object):
    def __init__(self):
        self.database = DatabaseName.STOCK_BASE_DATA.value
        self.a_share_capitalization = pd.DataFrame.empty

    def update_a_share_capitalization(self):
        """
        保存 总股本,总市值, 流通股本,流通市值 四个hdf5
        :return:
        """
        with MongoConnect(self.database):
            a_share_capitalization = AShareCapitalization.objects().as_pymongo()
            field_list = ['security_code', 'change_date', 'total_share', 'float_share', 'float_a_share',
                          'float_b_share', 'float_h_share']
            self.a_share_capitalization = pd.DataFrame(list(a_share_capitalization)).reindex(columns=field_list)


            # folder_name = LocalDataFolderName.INDEX_MEMBER.value
            # path = LocalDataPath.path + folder_name + '/'
            # data_name = folder_name
            # save_data_to_hdf5(path, data_name, self.index_members_df)


if __name__ == '__main__':
    share_capitalization_obj = UpAShareCapitalization()
    share_capitalization_obj.update_a_share_capitalization()