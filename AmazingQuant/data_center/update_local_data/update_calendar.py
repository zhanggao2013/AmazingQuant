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

    def save_calendar_hdf5(self):
        connection.connect(db=self.database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        data = AShareCalendar.objects().as_pymongo()
        data_df = pd.DataFrame(data)
        data_df.set_index('market', inplace=True)
        data_df = data_df.drop(['_id', 'update_date'], axis=1)
        # data_df['trade_days'] = data_df['trade_days'].apply(lambda x: pickle.dumps(x, protocol=4))
        print(data_df.dtypes)
        path = '../../../../data/calendar/'
        data_name = 'a_share_calendar'
        # save_data_to_hdf5(path, data_name, data_df)
        if not os.path.exists(path):
            os.mkdir(path)
        hdf_store = pd.HDFStore(path + data_name + '.h5', mode='w')
        hdf_store.put(data_name, data_df, format='table', append=False)
        hdf_store.close()


if __name__ == '__main__':
    calendar_obj = UpdateCalendar()
    calendar_obj.save_calendar_hdf5()
    # print(result)





