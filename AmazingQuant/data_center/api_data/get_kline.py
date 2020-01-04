# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/30
# @Author  : gao
# @File    : get_kline.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

import pandas as pd

from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment, LocalDataFolderName
from AmazingQuant.utils.performance_test import Timer


class UpdateKlineData(object):
    def __init__(self):
        self.field = ['open', 'high', 'low', 'close', 'volume', 'amount', 'match_items']
        self.end = ''
        self.calendar_SZ = []

    def cache_all_stock_date(self):
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.A_SHARE.value
        path = '../../../../data/' + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
        all_market_date = {}
        for i in self.field:
            data_name = i + '.h5'
            all_market_date[i] = pd.read_hdf(path + data_name)
        return all_market_date

    def get_market_data(self, market_data, stock_code=None, field=None, start=None, end=None, period=Period.DAILY.value, count=-1):
        result = None
        if len(stock_code) == 1 and len(field) == 1 and (start < end) and count == -1:
            result = market_data[field[0]][stock_code[0]][start: end]
        elif len(stock_code) == 1 and len(field) == 1 and (start == end) and count == -1:
            result = market_data[field[0]][stock_code[0]][start]
        elif len(stock_code) > 1 and (start == end) and count == -1:
            result = {i: market_data[i].reindex(columns=stock_code).loc[start] for i in field}
        elif len(stock_code) > 1 and (start != end) and count == -1:
            result = {i: market_data[i].reindex(columns=stock_code).loc[start: end] for i in field}
        return result

    def cache_all_index_data(self):
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.INDEX.value
        path = '../../../../data/' + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
        index_date = {}
        for i in self.field:
            data_name = i + '.h5'
            index_date[i] = pd.read_hdf(path + data_name)
        return index_date
    
    def get_index_data(self, index_data, index_code=None, field=None, start=None, end=None, period=Period.DAILY.value, count=-1):
        return self.get_market_data(index_data, stock_code=index_code, field=field, start=start, end=end, period=period, count=count)


if __name__ == '__main__':
    with Timer(True):
        kline_object = UpdateKlineData()
        all_market_data = kline_object.cache_all_stock_date()
        all_index_data = kline_object.cache_all_index_data()
        
        index_data = kline_object.get_index_data(all_index_data, index_code=['000001.SH'], field=['open', 'close'], end=datetime.now())
        market_data = kline_object.get_market_data(all_market_data, stock_code=['600000.SH'], field=['open', 'close'],
                                                   start=datetime(2019, 7, 5), end=datetime(2019, 7, 5))
