# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/16
# @Author  : gao
# @File    : save_kline_daily.py
# @Project : AmazingQuant 

from datetime import datetime
import os
from multiprocessing import Pool, Manager

import pandas as pd
import numpy as np
from mongoengine.context_managers import switch_collection

from AmazingQuant.data_center.mongo_connection_me import MongoConnect
from AmazingQuant.utils.performance_test import Timer
from apps.server.database_field.field_a_share_kline import Kline
from AmazingQuant.utils.security_type import is_security_type
from AmazingQuant.constant import DatabaseName


class SaveKlineDaily(object):
    def __init__(self, data_path, data_dict):
        self.data_path = data_path
        self.data_dict = data_dict
        self.database = DatabaseName.A_SHARE_KLINE_DAILY.value

        self.security_code_list = []
        self.market_list = ['SZ', 'SH']

    def insert_security_code_list(self):
        stock_code_list = []
        for market in self.market_list:
            path = self.data_path + market + '/MultDate/'
            file_list = os.listdir(path)
            stock_code_list += [i.split('.')[0] + '.' + market for i in file_list]
            file_num = 0
            p = Pool(8)
            for file_name in file_list:
                file_num += 1
                print('完成数量：', file_num)
                p.apply_async(self.insert_security_code, args=(market, file_name, path))
            p.close()
            p.join()

        delist = list(set(self.data_dict.keys()).difference(set(stock_code_list)))
        with MongoConnect(self.database):
            for security_code in delist:
                with switch_collection(Kline, security_code) as KlineDaily_security_code:
                    doc_list = []
                    security_code_data = self.data_dict[security_code].set_index(["TRADE_DT"])
                    for index, row in security_code_data.iterrows():
                        if row['S_DQ_AMOUNT'] > 0:
                            date_int = int(index)
                            date_int = str(date_int)
                            time_tag = datetime.strptime(date_int, "%Y%m%d")
                            try:
                                pre_close = int(row['S_DQ_PRECLOSE'] * 10000)
                            except KeyError:
                                pre_close = None
                            doc = KlineDaily_security_code(time_tag=time_tag, pre_close=pre_close,
                                                           open=int(row['S_DQ_OPEN'] * 10000),
                                                           high=int(row['S_DQ_HIGH'] * 10000),
                                                           low=int(row['S_DQ_LOW'] * 10000),
                                                           close=int(row['S_DQ_CLOSE'] * 10000),
                                                           volume=int(row['S_DQ_VOLUME'] * 100),
                                                           amount=int(row['S_DQ_AMOUNT'] * 1000),
                                                           match_items=0, interest=0)
                            doc_list.append(doc)
                    KlineDaily_security_code.objects.insert(doc_list)

    def insert_security_code(self, market, file_name, path):
        with MongoConnect(self.database):
            print(path + file_name + '\n')
            kline_daily_data = pd.read_csv(path + file_name, encoding='unicode_escape')
            security_code = file_name.split('.')[0] + '.' + market
            if is_security_type(security_code, 'EXTRA_STOCK_A'):
                kline_daily_data = kline_daily_data.reindex(columns=['date', 'open', 'high', 'low', 'close', 'volumw',
                                                                     'turover', 'match_items', 'interest'])
                kline_daily_data.rename(columns={'volumw': 'volume', 'turover': 'amount'},  inplace=True)
                kline_daily_data = kline_daily_data[kline_daily_data.date >= 20020104]
                with switch_collection(Kline, security_code) as KlineDaily_security_code:
                    doc_list = []
                    security_code_data = pd.DataFrame()
                    if security_code in self.data_dict.keys():
                        security_code_data = self.data_dict[security_code].set_index(["TRADE_DT"])
                        security_code_data = security_code_data.fillna(0)
                    for index, row in kline_daily_data.iterrows():
                        date_int = int(row['date'])
                        if not np.isnan(date_int):
                            try:
                                pre_close = int(10000 * security_code_data.loc[date_int, 'S_DQ_PRECLOSE'])
                            except KeyError:
                                pre_close = None
                            date_int = str(date_int)
                            time_tag = datetime.strptime(date_int, "%Y%m%d")
                            doc = KlineDaily_security_code(time_tag=time_tag, pre_close=pre_close,
                                                           open=int(row['open']), high=int(row['high']),
                                                           low=int(row['low']), close=int(row['close']),
                                                           volume=int(row['volume']), amount=int(row['amount']),
                                                           match_items=int(row['match_items']), interest=int(row['interest']))
                            doc_list.append(doc)

                    # 用csv全表补充20020104之前的日线数据，match_items为0
                    security_code_data = security_code_data[security_code_data.index < 20020104]
                    for index, row in security_code_data.iterrows():
                        if row['S_DQ_AMOUNT'] > 0:
                            date_int = int(index)
                            date_int = str(date_int)
                            time_tag = datetime.strptime(date_int, "%Y%m%d")
                            try:
                                pre_close = int(row['S_DQ_PRECLOSE'] * 10000)
                            except KeyError:
                                pre_close = None
                            doc = KlineDaily_security_code(time_tag=time_tag, pre_close=pre_close,
                                                           open=int(row['S_DQ_OPEN'] * 10000),
                                                           high=int(row['S_DQ_HIGH'] * 10000),
                                                           low=int(row['S_DQ_LOW'] * 10000),
                                                           close=int(row['S_DQ_CLOSE'] * 10000),
                                                           volume=int(row['S_DQ_VOLUME'] * 100),
                                                           amount=int(row['S_DQ_AMOUNT'] * 1000),
                                                           match_items=0, interest=0)
                            doc_list.append(doc)
                    KlineDaily_security_code.objects.insert(doc_list)


if __name__ == '__main__':
    with Timer(True):
        with Manager() as manager:
            data_df = pd.read_csv('../../../../data/KLine_daily/ASHAREEODPRICES.csv', low_memory=False)
            grouped = data_df.groupby("S_INFO_WINDCODE")
            data_dict = manager.dict({str(i[0]): i[1].reset_index(drop=True) for i in grouped})

            save_kline_object = SaveKlineDaily('../../../../data/KLine_daily/KLine/', data_dict)

            save_kline_object.insert_security_code_list()
