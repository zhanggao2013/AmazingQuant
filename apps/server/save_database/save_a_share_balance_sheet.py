# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/21
# @Author  : gao
# @File    : save_a_share_balance_sheet.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd
import numpy as np
from mongoengine.fields import DateTimeField, StringField

from apps.server.database_field.field_a_share_finance_data import AShareBalanceSheet
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.utils.transfer_field import get_collection_property_list


class SaveBalanceSheet(object):
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.collection_property_list = get_collection_property_list(AShareBalanceSheet)

    def save_a_share_balance_sheet(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)
                row_dict['security_code'] = row_dict['S_INFO_WINDCODE']
                row_dict.pop('WIND_CODE')
                row_dict.pop('OBJECT_ID')
                row_dict.pop('S_INFO_WINDCODE')

                doc = AShareBalanceSheet()

                for key, value in row_dict.items():
                    if key.lower() in self.collection_property_list:
                        property_name = AShareBalanceSheet.__dict__[key.lower()]
                        if isinstance(property_name, StringField):
                            setattr(doc, key.lower(), str(value))
                        elif isinstance(property_name, DateTimeField):
                            if np.isnan(value):
                                setattr(doc, key.lower(), None)
                            else:
                                setattr(doc, key.lower(), datetime.strptime(str(int(value)), "%Y%m%d"))
                        else:
                            setattr(doc, key.lower(), value)

                doc_list.append(doc)
                if len(doc_list) > 999:
                    AShareBalanceSheet.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareBalanceSheet.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/AShareBalanceSheet.csv'
    save_balance_sheet_obj = SaveBalanceSheet(data_path)
    save_balance_sheet_obj.save_a_share_balance_sheet()
