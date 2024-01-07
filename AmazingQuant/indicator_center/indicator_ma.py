# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/19
# @Author  : gao
# @File    : indicator_ma.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd
import numpy as np
import talib

from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.constant import RightsAdjustment
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.indicator_center.save_get_indicator import SaveGetIndicator
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login


class MaIndicator(object):
    def __init__(self):
        self.kline = pd.DataFrame({})
        self.stock_list = []

    def get_stock_list(self):
        tgw_api_object = TgwApiData(20991231)
        self.stock_list = tgw_api_object.get_code_list(add_market=True, all_code=True)
        return self.stock_list

    def get_kline_data(self):
        kline_data = GetKlineData()
        all_stock_data = kline_data.cache_all_stock_data(dividend_type=RightsAdjustment.FROWARD.value)
        self.kline = kline_data.get_market_data(all_stock_data, stock_code=self.stock_list, field=['close'])
        return self.kline

    def save_ma(self, num):
        save_get_indicator = SaveGetIndicator()
        ma = self.kline['close'].rolling(num).mean()
        save_get_indicator.save_indicator('ma'+str(num), ma)
        return ma


if __name__ == '__main__':
    tgw_login()
    with Timer(True):
        ma_indicator = MaIndicator()
        ma_indicator.get_stock_list()
        print(len(ma_indicator.stock_list))
        ma_indicator.get_kline_data()
        ma5 = ma_indicator.save_ma(5)
        ma10 = ma_indicator.save_ma(10)
        save_get_indicator = SaveGetIndicator()
        a = save_get_indicator.get_indicator('ma5')
