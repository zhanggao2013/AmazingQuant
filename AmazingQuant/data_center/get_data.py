# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.data_center.mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName, Period


class GetMarketData(object):
    def __init__(self):
        self.conn = MongoConn()
        self.universe = ["000300.SH"]
        self.start = "20170101"
        self.end = "20170504"
        self.period = "daily"

    def get_benchmark_index(self, benckmark="", start="", end="", period=Period.DAILY.value):
        if period == Period.DAILY.value:
            self.db_name = DatabaseName.MARKET_DATA_DAILY.value
            benchmark_index = self.conn.select_colum(self, db_name=self.db_name, table=benckmark, value="timetag", colum)
        elif period == Period.ONE_MIN.value:
            self.db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
            self.db = self.conn.connect_db(self.db_name)

        return benchmark_index

if __name__ == "__main__":
    aa = GetMarketData()
    BB = aa.get_benchmark_index(benckmark="000300.SH")
    print(BB)

#(self.universe, self.start, self.end, self.period, self.rights_adjustment)
