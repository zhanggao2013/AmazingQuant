# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : save_a_share_calendar.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from apps.server.database_server.database_field import AShareCalendar
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from AmazingQuant.utils.data_transfer import date_to_datetime
from AmazingQuant.constant import DatabaseName


class SaveCalendar(object):
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)

    def save_a_share_calendar(self):
        database = DatabaseName.STOCK_BASE_DATA.value
        with MongoConnect(database):
            doc_list = []
            data_grouped = self.data_df.groupby("S_INFO_EXCHMARKET")
            data_dict = {i[0]: list(i[1]['TRADE_DAYS']) for i in data_grouped}
            for market, trade_days in data_dict.items():
                if market == 'SSE':
                    market = 'SH'
                elif market == 'SZSE':
                    market = 'SZ'
                trade_days = [date_to_datetime(str(i)) for i in sorted(trade_days)]
                doc = AShareCalendar(market=market, trade_days=trade_days)
                doc_list.append(doc)
            AShareCalendar.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../../data/finance/ASHARECALENDAR.csv'
    save_calendar_obj = SaveCalendar(data_path)
    save_calendar_obj.save_a_share_calendar()
