# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/12
# @Author  : gao
# @File    : save_index_kline_daily.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime
import os
from multiprocessing import Pool

import pandas as pd
import numpy as np
from mongoengine.context_managers import switch_collection

from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.utils.performance_test import Timer
from apps.server.database_server.database_field.field_a_share_kline import Kline
from AmazingQuant.constant import DatabaseName


class SaveIndexKlineDaily(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.market_list = ['SZ', 'SH']

    def insert_security_code_list(self):
        for market in self.market_list:
            path = self.data_path + market + '/MultDate/'
            file_list = os.listdir(path)
            file_num = 0
            p = Pool(8)
            for file_name in file_list:
                file_num += 1
                print('完成数量：', file_num)
                p.apply_async(self.insert_security_code, args=(market, file_name, path))
                # self.insert_security_code(market, file_name, path)
            p.close()
            p.join()

    def insert_security_code(self, market, file_name, path):
        database = DatabaseName.INDEX_KLINE_DAILY.value
        with MongoConnect(database):
            print(path + file_name + '\n')
            kline_daily_data = pd.read_csv(path + file_name, encoding='unicode_escape')
            code = file_name.split('.')[0]
            code_transfer_dict = {'999999': '000001', '999998': '000002', '999997': '000003', '999996': '000004',
                                  '999995': '000005', '999994': '000006', '999993': '000007', '999992': '000008',
                                  '999991': '000010', '999990': '000011', '999989': '000012', '999988': '000013',
                                  '999987': '000016', '999986': '000015', '000300': '000300'}
            if market == 'SH':
                if code in code_transfer_dict.keys():
                    code = code_transfer_dict[code]
                else:
                    code = '00' + code[2:]
            security_code = code + '.' + market
            kline_daily_data = kline_daily_data.reindex(columns=['date', 'open', 'high', 'low', 'close', 'volumw',
                                                                 'turover', 'match_items', 'interest'])
            kline_daily_data.rename(columns={'volumw': 'volume', 'turover': 'amount'},  inplace=True)

            with switch_collection(Kline, security_code) as KlineDaily_security_code:
                doc_list = []
                for index, row in kline_daily_data.iterrows():
                    date_int = int(row['date'])
                    if not np.isnan(date_int):
                        date_int = str(date_int)
                        time_tag = datetime.strptime(date_int, "%Y%m%d")
                        doc = KlineDaily_security_code(time_tag=time_tag, pre_close=None,
                                                       open=int(row['open']), high=int(row['high']),
                                                       low=int(row['low']), close=int(row['close']),
                                                       volume=int(row['volume']), amount=int(row['amount']),
                                                       match_items=int(row['match_items']), interest=int(row['interest']))
                        doc_list.append(doc)

                KlineDaily_security_code.objects.insert(doc_list)


if __name__ == '__main__':
    with Timer(True):
        save_index_kline_object = SaveIndexKlineDaily('../../../../../data/KLine_daily/KLine_index_daily/')
        save_index_kline_object.insert_security_code_list()
