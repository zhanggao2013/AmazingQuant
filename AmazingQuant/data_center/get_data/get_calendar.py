# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : get_calendar.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.data_center.database_field.filed_a_share_calendar import AShareCalendar
from AmazingQuant.constant import DatabaseName


class GetCalendar(object):
    def __init__(self):
        pass

    def get_calendar(self, market):
        database = DatabaseName.STOCK_BASE_DATA.value
        with MongoConnect(database):
            data = AShareCalendar.objects(market=market).as_pymongo()
            trade_days = data[0]['trade_days']
            trade_days = [i for i in trade_days if i < datetime.now()]
            return trade_days


if __name__ == '__main__':
    calendar_obj = GetCalendar()
    result = calendar_obj.get_calendar('SH')
    print(result)





