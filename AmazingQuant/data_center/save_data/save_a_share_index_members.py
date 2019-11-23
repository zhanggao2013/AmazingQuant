# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/22
# @Author  : gao
# @File    : save_a_share_index_members.py
# @Project : AmazingQuant
# ------------------------------


import pandas as pd
import numpy as np

from AmazingQuant.data_center.database_field.field_a_share_index_members import AShareIndexMembers
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class SaveAShareIndexMembers(object):
    def __init__(self, data_path, field_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.field_is_str_list = get_field_str_list(field_path)

    def save_a_share_index_members(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)

                row_dict['index_code'] = row_dict['S_INFO_WINDCODE']
                row_dict['security_code'] = row_dict['S_CON_WINDCODE']
                row_dict['in_date'] = row_dict['S_CON_INDATE']
                row_dict['out_date'] = row_dict['S_CON_OUTDATE']
                row_dict['current_sign'] = row_dict['CUR_SIGN']

                row_dict.pop('OBJECT_ID')
                row_dict.pop('S_INFO_WINDCODE')
                row_dict.pop('S_CON_WINDCODE')
                row_dict.pop('S_CON_INDATE')
                row_dict.pop('S_CON_OUTDATE')
                row_dict.pop('CUR_SIGN')

                doc = AShareIndexMembers()
                for key, value in row_dict.items():
                    if key.lower() in self.field_is_str_list:
                        if key.lower() in ['s_con_indate', 's_con_outdate', 'current_sign']:
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
                    AShareIndexMembers.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareIndexMembers.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/AINDEXMEMBERS.csv'
    field_path = '../../config/field_a_share_index_members.txt'
    save_cash_flow_obj = SaveAShareIndexMembers(data_path, field_path)
    save_cash_flow_obj.save_a_share_index_members()
