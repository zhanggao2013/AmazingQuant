# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : update_calendar.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from AmazingQuant.config.local_data_path import LocalDataPath
from apps.server.database_field.filed_a_share_calendar import AShareCalendar
from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.mongo_connection_me import MongoConnect


class UpdateCalendar(object):
    def __init__(self):
        self.database = DatabaseName.STOCK_BASE_DATA.value

    def update_calendar_hdf5(self):
        with MongoConnect(self.database):
            data = AShareCalendar.objects().as_pymongo()
            data_df = pd.DataFrame(data)
            data_df.set_index('market', inplace=True)
            data_df = data_df.drop(['_id', 'update_date'], axis=1)
            folder_name = LocalDataFolderName.CALENDAR.value
            for index, row in data_df.iterrows():
                path = LocalDataPath.path + folder_name + '/'
                data_name = folder_name + '_' + str(index)
                save_data_to_hdf5(path, data_name, pd.DataFrame(data_df.loc[index, 'trade_days']))


if __name__ == '__main__':
    calendar_obj = UpdateCalendar()
    calendar_obj.update_calendar_hdf5()
    # print(result)





