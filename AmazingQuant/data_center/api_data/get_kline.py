# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/30
# @Author  : gao
# @File    : get_kline.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime
from multiprocessing import Pool, Manager, cpu_count

import pandas as pd
from mongoengine.context_managers import switch_collection
from mongoengine import connection

from AmazingQuant.config.database_info import MongodbConfig
from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment
from AmazingQuant.data_center.database_field.field_a_share_kline import Kline
from AmazingQuant.data_center.api_data.get_calender import GetCalendar
from AmazingQuant.utils.performance_test import Timer


class UpdateKlineData(object):
    def __init__(self):
        self.field = []
        self.end = ''
        self.calendar_SZ = []

    def get_index_data(self, index_list=[], field=[], start="", end=datetime.now(), period=Period.DAILY.value):
        pass

    def get_market_data(self, market_data, stock_code=[], field=[], start=None, end=None, period=Period.DAILY.value, count=-1):
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


if __name__ == '__main__':
    from AmazingQuant.utils.security_type import is_security_type
    stock_code_a_share = [i for i in stock_code if is_security_type(i, 'EXTRA_STOCK_A')]
    print(len(stock_code_a_share))
    with Timer(True):
        kline_object = UpdateKlineData()
        all_market_data = kline_object.get_all_market_data(security_list=stock_code_a_share,
                                                           end=datetime.now())
        # for i in all_market_data:
        #     all_market_data[i].to_hdf(i+'.h5', key=i)
        # index_data = kline_object.get_index_data(index_list=['000001.SH'], field=['open', 'close'], end=datetime.now())
        # market_data = kline_object.get_market_data(all_market_data, stock_code=a[:20], field=['open', 'close'],
        #                                            start=datetime(2019, 7, 5), end=datetime(2019, 7, 5))
