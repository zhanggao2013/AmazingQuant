# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/16
# @Author  : gao
# @File    : save_kline_daily.py
# @Project : AmazingQuant 

from datetime import datetime
import os
from multiprocessing import Pool

import pandas as pd
import numpy as np
from mongoengine import Document
from mongoengine.fields import DictField, ListField, StringField, FloatField, IntField, DateTimeField
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.performance_test import Timer


class KlineDaily(Document):
    update_date = DateTimeField(default=datetime.utcnow())
    security_code = StringField(required=True)
    date = IntField(required=True)
    time_tag = IntField(required=True)
    data = ListField(required=True)
    meta = {'indexes': ['security_code', 'time_tag'], 'shard_key': ('security_code', 'time_tag',)}


class SaveKlineDaily(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.security_code_list = []
        self.market_list = ['SH', 'SZ']

    def insert_security_code_list(self):
        for market in self.market_list:
            path = self.data_path + market + '/MultDate/'
            file_list = os.listdir(path)
            file_num = 0
            p = Pool(20)
            for file_name in file_list:
                file_num += 1
                print('完成数量：', file_num)
                p.apply_async(self.insert_security_code, args=(market, file_name, path))
                # self.insert_security_code(market, file_name, path)

    def insert_security_code(self, market, file_name, path):
        database = 'kline'
        with MongoConnect(database):
            print(path + file_name + '\n')
            kline_daily_data = pd.read_csv(path + file_name, encoding='unicode_escape')
            date = kline_daily_data['date'][0]
            if not np.isnan(date):
                time_tag = kline_daily_data['time'][0]
                security_code = file_name.split('.')[0] + '.' + market
                kline_daily_data = kline_daily_data.reindex(columns=['open', 'high', 'low', 'close', 'volumw',
                                                                     'turover', 'match_items', 'interest'])
                kline_daily_data.rename(columns={'volumw': 'volume', 'turover': 'amount'},  inplace=True)
                doc_list = []
                for index, row in kline_daily_data.iterrows():
                    data = [int(value) for value in dict(row).values()]
                    data = [int(row['open']), int(row['high']), int(row['low']), int(row['close']), int(row['volume']),
                            int(row['amount']), int(row['match_items']), int(row['interest']), ]
                    doc = KlineDaily(security_code=security_code,
                                     date=int(date),
                                     time_tag=int(time_tag),
                                     data=data)
                    doc_list.append(doc)
                KlineDaily.objects.insert(doc_list)


if __name__ == '__main__':
    with Timer(True):
        save_kline_object = SaveKlineDaily('../../../../data/KLine_daily/KLine/')
        save_kline_object.insert_security_code_list()
