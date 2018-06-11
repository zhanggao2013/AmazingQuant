# -*- coding: utf-8 -*-

__author__ = "gao"
import time

from AmazingQuant.data_center.mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName, Period


class GetMarketData(object):
    def __init__(self):
        self.conn = MongoConn()
        self.universe = ["000300.SH"]
        self.start = "20170101"
        self.end = "20170504"
        self.period = "daily"

    def date_to_milisecond(self, date="2010-01-01"):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

    def milisecond_to_date(self, milisecond=1262275200):
        return time.strftime("%Y%m%d", time.localtime(milisecond))

    def date_str_to_int(self, date="2010-01-01"):
        return int(date.replace("-", ""))

    def get_benchmark_index(self, benckmark="", start="", end="", period=Period.DAILY.value):
        if period == Period.DAILY.value:
            self.db_name = DatabaseName.MARKET_DATA_DAILY.value
            start = self.date_str_to_int(start)
            end = self.date_str_to_int(end)

            print(start, end)
            benchmark_index = self.conn.select_colum(db_name=self.db_name, table=benckmark,
                                                     value={"timetag": {"$gte": start, "$lte": end}}, colum="timetag")
            benchmark_index_list = []
            for x in benchmark_index:
                benchmark_index_list.append(int(x["timetag"]))
        elif period == Period.ONE_MIN.value:
            self.db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
            self.db = self.conn.connect_db(self.db_name)

        return benchmark_index_list
    # def get_all_market_data(self,universe=[], start=0):


if __name__ == "__main__":
    aa = GetMarketData()
    BB = aa.get_benchmark_index(benckmark="000300.SH", start="2017-01-01", end="2017-01-09")
    print(BB)
    print(type(aa.milisecond_to_date()))
    print(int(("2017-01-01").replace("-", "")))
