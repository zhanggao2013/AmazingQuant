# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/22
# @Author  : gao
# @File    : save_a_share_profit_express.py
# @Project : AmazingQuant
# ------------------------------



import pandas as pd
import numpy as np

from AmazingQuant.data_center.database_field.field_finance_data import AShareProfitExpress
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class SaveProfitExpress(object):
    def __init__(self, data_path, field_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.field_is_str_list = get_field_str_list(field_path)

    def save_a_share_profit_express(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)
                row_dict['security_code'] = row_dict['S_INFO_WINDCODE']
                row_dict.pop('OBJECT_ID')
                row_dict.pop('S_INFO_WINDCODE')

                doc = AShareProfitExpress()
                for key, value in row_dict.items():
                    if key.lower() in self.field_is_str_list:
                        if key.lower() in ['ann_dt', 'report_period', 'actual_ann_dt']:
                            if np.isnan(value):
                                setattr(doc, key.lower(), -1)
                            else:
                                setattr(doc, key.lower(), int(value))
                        else:
                            setattr(doc, key.lower(), str(value))
                    else:
                        setattr(doc, key.lower(), value)
                doc_list.append(doc)
                if len(doc_list) > 999:
                    AShareProfitExpress.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareProfitExpress.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/ASHAREPROFITEXPRESS.csv'
    field_path = '../../config/field_a_share_profit_express.txt'
    save_cash_flow_obj = SaveProfitExpress(data_path, field_path)
    save_cash_flow_obj.save_a_share_profit_express()
