# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/19
# @Author  : gao
# @File    : get_kline.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime
import os
from multiprocessing import Pool, Queue, Manager
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import numpy as np
from mongoengine.context_managers import switch_collection

from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment
from AmazingQuant.data_center.database_field.field_a_share_kline import Kline
from AmazingQuant.utils.performance_test import Timer


class GetKlineData(object):
    def __init__(self):
        self.field = []
        self.end = datetime.now()

    def get_all_market_data(self, stock_list=[], field=[], start="", end=datetime.now(), period=Period.DAILY.value,
                            rights_adjustment=RightsAdjustment.NONE.value):
        """

        :param stock_list:
        :param field: 默认['time_tag', 'open', 'high', 'low', 'close', 'volume', 'amount', 'match_items', 'interest']
        :param start:
        :param end:
        :param period:
        :param rights_adjustment:
        :return:
        """
        self.field = ['time_tag'] + field
        if len(self.field) == 1:
            self.field = ['time_tag', 'open', 'high', 'low', 'close', 'volume', 'amount', 'match_items', 'interest']
        self.end = end
        database = DatabaseName.A_SHARE_KLINE_DAILY.value
        process_num = 6
        process_pool = Pool(process_num)
        process_stock_num = int(len(stock_list) / process_num) + 1
        stock_list_split = []
        for i in range(int(len(stock_list) / process_stock_num)):
            if i < int(len(stock_list) / process_stock_num)-1:
                stock_list_split.append(stock_list[i * process_stock_num: (i + 1) * process_stock_num])
            else:
                stock_list_split.append(stock_list[i * process_stock_num:])

        with Manager() as manager:
            process_manager_dict = manager.dict()
            for stock_list_i in range(len(stock_list_split)):
                process_pool.apply_async(self.get_data_with_process_pool, args=(database, stock_list_split[stock_list_i], process_manager_dict, stock_list_i))
            process_pool.close()
            process_pool.join()
            process_dict = dict(process_manager_dict)
            result = {}
            for value in process_dict.values():
                result.update(value)
            print(result)
            return pd.concat(list(result.values()), keys=list(result.keys()))

    def get_data_with_process_pool(self, database, stock_list, process_manager_dict, stock_list_i):
        with MongoConnect(database):
            thread_data_dict = {}
            with ThreadPoolExecutor(4) as executor:
                for stock in stock_list:
                    executor.submit(self.get_data_with_thread_pool, stock, thread_data_dict)
            process_manager_dict[stock_list_i] = thread_data_dict

    def get_data_with_thread_pool(self, stock, thread_data_dict):
        with switch_collection(Kline, stock) as KlineDaily_security_code:
            # KlineDaily_security_code.drop_collection()
            security_code_data = KlineDaily_security_code.objects(time_tag__lte=self.end).as_pymongo()
            security_code_data_df = pd.DataFrame(list(security_code_data)).reindex(
                columns=self.field)
            security_code_data_df.set_index(["time_tag"], inplace=True)
            # print('KlineDaily_security_code', stock)
            thread_data_dict[stock] = security_code_data_df


if __name__ == '__main__':
    with Timer(True):
        kline_object = GetKlineData()
        a = kline_object.get_all_market_data(stock_list=['600000.SH'], field=['close'], end=datetime(2018, 10, 10))
