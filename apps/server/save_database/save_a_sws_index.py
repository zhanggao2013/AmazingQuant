# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/11
# @Author  : gao
# @File    : save_a_sws_index.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd
import numpy as np

from apps.server.database_field.field_a_sws_index import ASwsIndex
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.utils.data_transfer import date_to_datetime


class SaveASwsIndex(object):
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)

    def save_a_sw_index(self):
        database = 'stock_base_data'

        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row = dict(row)
                for filed, value in row.items():
                    if filed in ['S_DQ_PRECLOSE', 'S_DQ_OPEN', 'S_DQ_HIGH', 'S_DQ_LOW', 'S_DQ_CLOSE']:
                        if not np.isnan(value):
                            row[filed] = int(row[filed] * 10000)
                    elif filed in ['S_DQ_VOLUME']:
                        if not np.isnan(value):
                            row[filed] = int(row[filed] * 100)
                    elif filed in ['S_DQ_AMOUNT']:
                        if not np.isnan(value):
                            row[filed] = int(row[filed] * 1000)

                doc = ASwsIndex(sw_index_code=row['S_INFO_WINDCODE'],
                                time_tag=date_to_datetime(str(row['TRADE_DT'])),
                                pre_close=row['S_DQ_PRECLOSE'],
                                open=row['S_DQ_OPEN'],
                                high=row['S_DQ_HIGH'],
                                low=row['S_DQ_LOW'],
                                close=row['S_DQ_CLOSE'],
                                volume=row['S_DQ_VOLUME'],
                                amount=row['S_DQ_AMOUNT'],
                                index_pe=row['S_VAL_PE'],
                                index_pb=row['S_VAL_PB'],
                                index_free_float_market_capitalisation=row['S_DQ_MV'],
                                index_total_market_capitalisation=row['S_VAL_MV'])
                doc_list.append(doc)
                if len(doc_list) > 999:
                    ASwsIndex.objects.insert(doc_list)
                    doc_list = []
            else:
                ASwsIndex.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/ASWSINDEXEOD.csv'
    save_a_sws_obj = SaveASwsIndex(data_path)
    save_a_sws_obj.save_a_sw_index()

