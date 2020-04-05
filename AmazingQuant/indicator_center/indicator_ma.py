# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/19
# @Author  : gao
# @File    : indicator_ma.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd
import numpy as np
# import talib

from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.data_center.api_data.get_index_member import GetIndexMember
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator


class MaIndicator(object):
    def __init__(self):
        self.kline = pd.DataFrame({})
        self.stock_list = []

    def get_stock_list(self):
        index_member = GetIndexMember()
        index_member.get_all_index_members()
        _, stock_list_SH = index_member.get_index_members('000001.SH')
        _, stock_list_SZ = index_member.get_index_members('399106.SZ')
        self.stock_list = stock_list_SH + stock_list_SZ
        return self.stock_list

    def get_kline_data(self):
        kline_data = GetKlineData()
        all_stock_data = kline_data.cache_all_stock_data()
        self.kline = kline_data.get_market_data(all_stock_data, stock_code=self.stock_list, field=['close'])
        return self.kline

    def save_ma(self, num):
        save_get_indicator = SaveGetIndicator()
        ma5 = self.kline['close'].rolling(num).mean()
        save_get_indicator.save_indicator('ma'+str(num), ma5)
        pass


if __name__ == '__main__':
    with Timer(True):
        ma_indicator = MaIndicator()
        ma_indicator.get_stock_list()
        print(len(ma_indicator.stock_list))
        ma_indicator.get_kline_data()
        ma_indicator.save_ma(5)
        ma_indicator.save_ma(10)
        save_get_indicator = SaveGetIndicator()
        a = save_get_indicator.get_indicator('ma5')
