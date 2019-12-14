# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : get_calendar.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime
from mongoengine import connection

from AmazingQuant.config.database_info import MongodbConfig
from AmazingQuant.data_center.database_field.filed_a_share_calendar import AShareCalendar
from AmazingQuant.constant import DatabaseName


class GetCalendar(object):
    def __init__(self):
        self.database = DatabaseName.STOCK_BASE_DATA.value

    def get_calendar(self, market):
        connection.connect(db=self.database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        data = AShareCalendar.objects(market=market).as_pymongo()
        trade_days = data[0]['trade_days']
        trade_days = [i for i in trade_days if i < datetime.now()]
        connection.disconnect()
        return trade_days


if __name__ == '__main__':
    calendar_obj = GetCalendar()
    result = calendar_obj.get_calendar('SH')
    print(result)





