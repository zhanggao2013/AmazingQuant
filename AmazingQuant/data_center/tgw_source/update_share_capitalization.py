# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/23
# @Author  : gao
# @File    : update_share_capitalization.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd
from spyder.utils.bsdsocket import SZ

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.utils.data_transfer import date_to_datetime


class UpAShareCapitalization(object):
    def __init__(self):
        self.a_share_capitalization = pd.DataFrame.empty

    def update_a_share_capitalization(self):
        """
        保存 总股本, 总市值, 流通股本, 流通市值 四个hdf5
        :return:
        """
        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        self.a_share_capitalization = get_local_data(path, 'stock_struction.h5')
        kline_object = GetKlineData()
        market_close_data = kline_object.cache_all_stock_data()['close']
        self.a_share_capitalization['EX_CHANGE_DATE'] = self.a_share_capitalization['EX_CHANGE_DATE'].astype(int)
        self.a_share_capitalization['EX_CHANGE_DATE'] = self.a_share_capitalization['EX_CHANGE_DATE'].apply(lambda x:date_to_datetime(str(x)))

        index = list(set(market_close_data.index).union(set(self.a_share_capitalization['EX_CHANGE_DATE'])))
        index.sort()
        share_capitalization_grouped = self.a_share_capitalization.groupby('MARKET_CODE')

        total_share_list = []
        float_a_share_list = []
        a = 0
        for i in share_capitalization_grouped:
            data = i[1].sort_values(by=['EX_CHANGE_DATE'])
            data.drop_duplicates(subset=['EX_CHANGE_DATE'], keep='last', inplace=True, ignore_index=False)
            data = data.set_index('EX_CHANGE_DATE')
            total_share_list.append(data['TOT_SHARE'].reindex(index).rename(i[0]))
            float_a_share_list.append(data['FLOAT_A_SHARE'].reindex(index).rename(i[0]))
            a += 1
            print(a)
        total_share = pd.concat(total_share_list, axis=1)
        float_a_share = pd.concat(float_a_share_list, axis=1)

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
        return total_share


if __name__ == '__main__':
    share_capitalization_obj = UpAShareCapitalization()
    total_share = share_capitalization_obj.update_a_share_capitalization()
    # 000405.SZ
    folder_name = LocalDataFolderName.FINANCE.value
    path = LocalDataPath.path + folder_name + '/'
    a_share_capitalization = get_local_data(path, 'stock_struction.h5')
    a = a_share_capitalization[a_share_capitalization['MARKET_CODE'] == '000405.SZ'].sort_values(by=['EX_CHANGE_DATE'])
