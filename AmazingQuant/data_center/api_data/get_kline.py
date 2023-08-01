# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/30
# @Author  : gao
# @File    : get_kline.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

import numpy as np

from AmazingQuant.constant import Period, RightsAdjustment, LocalDataFolderName
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_adj_factor import GetAdjFactor
from AmazingQuant.data_center.api_data.get_data import get_local_data


class GetKlineData(object):
    def __init__(self):
        self.field = ['open', 'high', 'low', 'close', 'volume', 'amount']
        self.end = ''
        self.calendar_SZ = []
        self.adj_factor_obj = GetAdjFactor()

    def cache_all_stock_data(self, period=Period.DAILY.value, dividend_type=RightsAdjustment.NONE.value, field=None):
        if field is not None:
            self.field = field
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.A_SHARE.value
        path = LocalDataPath.path + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
        all_market_date = {}
        adj_factor = 1
        if dividend_type == RightsAdjustment.FROWARD.value:
            adj_factor = self.adj_factor_obj.get_adj_factor(RightsAdjustment.FROWARD.value)
            # print('adj_factor', adj_factor.shape)
        elif dividend_type == RightsAdjustment.BACKWARD.value:
            adj_factor = self.adj_factor_obj.get_adj_factor(RightsAdjustment.BACKWARD.value)
            # print('adj_factor', adj_factor.shape)
        for i in self.field:
            data_name = i + '.h5'
            data = get_local_data(path, data_name)
            if isinstance(adj_factor, int):
                all_market_date[i] = data
            else:
                if i in ['open', 'high', 'low', 'close']:
                    all_market_date[i] = data.multiply(adj_factor)
                else:
                    all_market_date[i] = data
        return all_market_date

    def get_market_data(self, market_data, stock_code=None, field=None, start=None, end=None, count=-1):
        result = None
        if stock_code is None and len(field) == 1:
            result = market_data[field[0]]
        elif len(stock_code) == 1 and len(field) == 1 and (end is None and start is None) and count == -1:
            result = market_data[field[0]][stock_code[0]]
        elif len(stock_code) == 1 and len(field) == 1 and start < end and count == -1:
            result = market_data[field[0]][stock_code[0]][start: end]
        elif len(stock_code) == 1 and len(field) == 1 and start == end and count == -1:
            result = market_data[field[0]][stock_code[0]][start]
        elif len(stock_code) > 1 and (start == end and start is not None) and count == -1:
            result = {i: market_data[i].reindex(columns=stock_code).loc[start] for i in field}
        elif len(stock_code) > 1 and (end is None and start is None) and count == -1:
            result = {i: market_data[i].reindex(columns=stock_code) for i in field}
        elif start != end and count == -1:
            result = {i: market_data[i].reindex(columns=stock_code).loc[start: end] for i in field}
        return result

    def cache_all_index_data(self, period=Period.DAILY.value):
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.INDEX.value
        path = LocalDataPath.path + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
        index_date = {}
        for i in self.field:
            data_name = i + '.h5'
            index_date[i] = get_local_data(path, data_name)
        return index_date
    
    def get_index_data(self, index_data, index_code=None, field=None, start=None, end=None, period=Period.DAILY.value, count=-1):
        return self.get_market_data(index_data, stock_code=index_code, field=field, start=start, end=end, count=count)


if __name__ == '__main__':
    with Timer(True):
        kline_object = GetKlineData()
        all_market_data = kline_object.cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value)
        a = all_market_data['close']
        b = a['003816.SZ']
        print(b)
        # all_index_data = kline_object.cache_all_index_data()
        #
        # index_data = kline_object.get_index_data(all_index_data, index_code=['000001.SH'], field=['open', 'close'], end=datetime.now())
        # market_data = kline_object.get_market_data(all_market_data, stock_code=['000503.SZ'], field=['close'],
        #                                            start=datetime(2017, 10, 5), end=datetime(2019, 7, 5))
