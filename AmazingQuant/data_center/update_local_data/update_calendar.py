# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : update_calendar.py
# @Project : AmazingQuant
# ------------------------------
import os
import pickle

import pandas as pd
from mongoengine import connection

from AmazingQuant.config.database_info import MongodbConfig
from AmazingQuant.data_center.database_field.filed_a_share_calendar import AShareCalendar
from AmazingQuant.constant import DatabaseName
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5


class UpdateCalendar(object):
    def __init__(self):
        self.database = DatabaseName.STOCK_BASE_DATA.value
        self.a = 1

    def save_calendar_hdf5(self):
        connection.connect(db=self.database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        data = AShareCalendar.objects().as_pymongo()
        data_df = pd.DataFrame(data)
        data_df.set_index('market', inplace=True)
        data_df = data_df.drop(['_id', 'update_date'], axis=1)
        for index, row in data_df.iterrows():
            path = '../../../../data/calendar/'
            data_name = 'calendar_' + str(index)
            save_data_to_hdf5(path, data_name, pd.DataFrame(data_df.loc[index, 'trade_days']))


if __name__ == '__main__':
    calendar_obj = UpdateCalendar()
    calendar_obj.save_calendar_hdf5()
    # print(result)





