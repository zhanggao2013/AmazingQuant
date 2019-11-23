# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/20
# @Author  : gao
# @File    : save_a_share_income.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd
import numpy as np

from AmazingQuant.data_center.database_field.field_finance_data import AShareIncome
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class SaveIncome(object):
    def __init__(self, data_path, field_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.field_is_str_list = get_field_str_list(field_path)

    def save_a_share_cash_flow(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)
                row_dict['security_code'] = row_dict['S_INFO_WINDCODE']
                row_dict.pop('WIND_CODE')
                row_dict.pop('OBJECT_ID')
                row_dict.pop('S_INFO_WINDCODE')

                doc = AShareIncome()
                for key, value in row_dict.items():
                    if key.lower() in self.field_is_str_list:
                        if key.lower() in ['ann_dt', 'report_period', 'statement_type', 'actual_ann_dt']:
                            if np.isnan(value):
                                setattr(doc, key.lower(), None)
                            else:
                                setattr(doc, key.lower(), str(int(value)))
                        else:
                            setattr(doc, key.lower(), str(value))
                    else:
                        setattr(doc, key.lower(), value)
                doc_list.append(doc)
                if len(doc_list) > 999:
                    AShareIncome.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareIncome.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/ASHAREINCOME.csv'
    field_path = '../../config/field_a_share_income.txt'
    save_cash_flow_obj = SaveIncome(data_path, field_path)
    save_cash_flow_obj.save_a_share_cash_flow()
