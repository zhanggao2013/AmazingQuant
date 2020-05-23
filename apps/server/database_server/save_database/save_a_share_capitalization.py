# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/23
# @Author  : gao
# @File    : save_a_share_capitalization.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime

import pandas as pd

from apps.server.database_server.database_field.field_a_share_capitalization import AShareCapitalization
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.constant import DatabaseName


class SaveShareCapitalization(object):
    def __init__(self, data_path):
        data_df = pd.read_csv(data_path, low_memory=False)
        self.data_df = data_df.where(data_df.notnull(), None)

    def save_share_capitalization(self):
        database = DatabaseName.STOCK_BASE_DATA.value
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                # row_dict = {'security_code': row['S_INFO_WINDCODE'],
                #             'change_date': datetime.strptime(str(int(row['CHANGE_DT'])), "%Y%m%d"),
                #             'total_share': row['TOT_SHR'],
                #             'float_share': row['FLOAT_SHR'],
                #             'float_a_share': row['FLOAT_A_SHR'],
                #             'float_b_share': row['FLOAT_B_SHR'],
                #             'float_h_share': row['FLOAT_H_SHR']}
                doc = AShareCapitalization(security_code=row['S_INFO_WINDCODE'],
                                           change_date=datetime.strptime(str(int(row['CHANGE_DT'])), "%Y%m%d"),
                                           total_share=row['TOT_SHR'],
                                           float_share=row['FLOAT_SHR'],
                                           float_a_share=row['FLOAT_A_SHR'],
                                           float_b_share=row['FLOAT_B_SHR'],
                                           float_h_share=row['FLOAT_H_SHR'])
                doc_list.append(doc)
            AShareCapitalization.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../../data/finance/ASHARECAPITALIZATION.csv'
    save_share_capitalization_obj = SaveShareCapitalization(data_path)
    save_share_capitalization_obj.save_share_capitalization()
