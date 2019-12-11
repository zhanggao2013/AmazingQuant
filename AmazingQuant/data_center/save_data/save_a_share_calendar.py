# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : save_a_share_calendar.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd

from AmazingQuant.data_center.database_field.filed_a_share_calendar import AShareCalendar
from AmazingQuant.data_center.mongo_connection import MongoConnect


class SaveCalendar(object):
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)

    def save_a_share_calendar(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            data_grouped = self.data_df.groupby("S_INFO_EXCHMARKET")
            data_dict = {i[0]: list(i[1]['TRADE_DAYS']) for i in data_grouped}
            print(data_dict)
            for market, trade_days in data_dict.items():
                if market == 'SHN':
                    market = 'SH'
                elif market == 'SZN':
                    market = 'SZ'
                doc = AShareCalendar(market=market, trade_days=trade_days)
                doc_list.append(doc)
            AShareCalendar.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/ASHARECALENDAR.csv'
    save_calendar_obj = SaveCalendar(data_path)
    save_calendar_obj.save_a_share_calendar()
