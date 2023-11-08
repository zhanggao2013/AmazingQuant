# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/23
# @Author  : gao
# @File    : update_share_capitalization.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from apps.server.database_server.database_field.field_a_share_capitalization import AShareCapitalization
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
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
            kline_object = GetKlineData()
            market_close_data = kline_object.cache_all_stock_data()['close']
            index = list(set(market_close_data.index).union(set(self.a_share_capitalization['change_date'])))
            index.sort()
            share_capitalization_grouped = self.a_share_capitalization.groupby('security_code')

            total_share = pd.DataFrame({})
            float_a_share = pd.DataFrame({})
            for i in share_capitalization_grouped:
                data = i[1].sort_values('change_date').set_index('change_date')
                try:
                    total_share[i[0]] = data['total_share'].reindex(index)
                    float_a_share[i[0]] = data['float_a_share'].reindex(index)
                except ValueError:
                    # 有四只票 change date 重复,需要手工清洗修正
                    # print(data[data.index.duplicated()])
                    total_share[i[0]] = data[data.index.duplicated()]['total_share'].reindex(index)
                    float_a_share[i[0]] = data[data.index.duplicated()]['float_a_share'].reindex(index)
            total_share = total_share.fillna(method='ffill').reindex(market_close_data.index)
            float_a_share = float_a_share.fillna(method='ffill').reindex(market_close_data.index)
            total_share_value = total_share.multiply(10000) * market_close_data
            float_a_share_value = float_a_share.multiply(10000) * market_close_data

            folder_name = LocalDataFolderName.INDICATOR_EVERYDAY.value
            path = LocalDataPath.path + folder_name + '/'
            save_data_to_hdf5(path, 'total_share', total_share)
            save_data_to_hdf5(path, 'float_a_share', float_a_share)
            save_data_to_hdf5(path, 'total_share_value', total_share_value)
            save_data_to_hdf5(path, 'float_a_share_value', float_a_share_value)


if __name__ == '__main__':
    share_capitalization_obj = UpAShareCapitalization()
    share_capitalization_obj.update_a_share_capitalization()
