# -*- coding: utf-8 -*-

__author__ = "gao"

import time
import pandas as pd

from AmazingQuant.data_center.mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment


class GetMarketData(object):
    def __init__(self):
        self.conn = MongoConn()
        self.universe = ["000300.SH"]
        self.start = "20170101"
        self.end = "20170504"
        self.period = "daily"

    def date_to_millisecond(self, date="20100101"):
        return int(time.mktime(time.strptime(date, '%Y%m%d')))

    def millisecond_to_date(self, millisecond):
        return time.strftime("%Y-%m-%d", time.localtime(millisecond))

    def date_str_to_int(self, date="2010-01-01"):
        return int(date.replace("-", ""))

    def get_benchmark_index(self, benckmark="", start="", end="", period=Period.DAILY.value):
        if period == Period.DAILY.value:
            self.db_name = DatabaseName.MARKET_DATA_DAILY.value
            start = self.date_str_to_int(start)
            end = self.date_str_to_int(end)
            benchmark_index = self.conn.select_colum(db_name=self.db_name, table=benckmark,
                                                     value={"timetag": {"$gte": start, "$lte": end}},
                                                     colum={"_id": 0, "timetag": 1, "close": 1})
            benchmark_index_list = []
            for x in benchmark_index:
                benchmark_index_list.append(self.date_to_millisecond(str(int(x["timetag"]))))
        elif period == Period.ONE_MIN.value:
            self.db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
            self.db = self.conn.connect_db(self.db_name)
        return benchmark_index_list

    def get_all_market_data(self, universe=[], field="open", end="", period=Period.DAILY.value,
                            rights_adjustment=RightsAdjustment.NONE.value):
        if period == Period.DAILY.value:
            self.db_name = DatabaseName.MARKET_DATA_DAILY.value
            end = self.date_str_to_int(end)
            values = {}
            for stockcode in universe:
                stockcode_market_data = self.conn.select_colum(db_name=self.db_name, table=stockcode,
                                                               value={"timetag": {"$lte": end}},
                                                               colum={"_id": 0, "timetag": 1, field: 1})
                df = pd.DataFrame(list(stockcode_market_data))
                values[stockcode] = pd.Series(df[field].values, index=df['timetag'])
            all_market_data = pd.DataFrame(values)
        elif period == Period.ONE_MIN.value:
            self.db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
            self.db = self.conn.connect_db(self.db_name)
        return all_market_data


if __name__ == "__main__":
    aa = GetMarketData()
    BB = aa.get_benchmark_index(benckmark="000300.SH", start="2017-01-01", end="2017-01-09")
    print(BB)
    print(type(aa.millisecond_to_date()))
    print(int(("2017-01-01").replace("-", "")))
