# -*- coding: utf-8 -*-

__author__ = "gao"

import pandas as pd

from AmazingQuant.data_center.mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment
import AmazingQuant.utils.data_transfer as data_transfer


class GetData(object):
    def __init__(self):
        self.conn = MongoConn()

    def get_all_market_data(self, stock_code=[], field=[], start="", end="", period=Period.DAILY.value):

        if period == Period.DAILY.value:
            db_name = DatabaseName.MARKET_DATA_DAILY.value
            end = data_transfer.date_str_to_int(end)
            values = []
            colum = {"_id": 0, "timetag": 1}
            for i in field:
                colum[i] = 1
            for stock in stock_code:
                stock_market_data = self.conn.select_colum(db_name=db_name, table=stock,
                                                           value={"timetag": {"$lte": end}},
                                                           colum=colum)
                df = pd.DataFrame(list(stock_market_data))
                values.append(pd.DataFrame(df[field].values, index=df['timetag'], columns=field))
            market_data = pd.concat(values, keys=stock_code)
        elif period == Period.ONE_MIN.value:
            db_name = DatabaseName.MARKET_DATA_ONE_MIN.value

        return market_data

    def get_market_data(self, market_data, stock_code=[], field=[], start="", end="", skip_paused=True,
                            rights_adjustment=RightsAdjustment.NONE.value, count=-1):
        """
        从dataframe解析数据成最终的数据格式，复权　count　skip_paused都在在这里做
        :param market_data:
        :param stock_code:
        :param field:
        :param start:
        :param end:
        :param skip_paused:
        :param rights_adjustment:
        :param count:
        :return:
        """
        pass

    def get_end_timetag(self, benckmark, period=Period.DAILY.value):
        if period == Period.DAILY.value:
            db_name = DatabaseName.MARKET_DATA_DAILY.value
        elif period == Period.ONE_MIN.value:
            db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
        colum = {"_id": 0, "timetag": 1}
        end_timetag_list = self.conn.select_colum(db_name=db_name, table=benckmark,
                                                  value={},
                                                  colum=colum)
        end_timetag = str(int(max([i["timetag"] for i in list(end_timetag_list)])))
        return end_timetag[:4] + "-" + end_timetag[4:6] + "-" + end_timetag[6:]


if __name__ == "__main__":
    aa = GetMarketData()
    BB = aa.get_benchmark_index(benckmark="000300.SH", start="2017-01-01", end="2017-01-09")
    print(BB)
    print(type(aa.millisecond_to_date()))
    print(int(("2017-01-01").replace("-", "")))
