# -*- coding: utf-8 -*-

__author__ = "gao"

import pandas as pd

from AmazingQuant.data_center.mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName, Period, RightsAdjustment
import AmazingQuant.utils.data_transfer as data_transfer


class GetData(object):
    def __init__(self):
        self.conn = MongoConn()

    def get_all_market_data(self, stock_code=[], field=[], start="", end="", period=Period.DAILY.value,
                            rights_adjustment=RightsAdjustment.NONE.value):
        """
        复权因子在这做
        :param stock_code:
        :param field:
        :param start:
        :param end:
        :param period:
        :param rights_adjustment:
        :return: 代码-n，字段-n，时间-n,  return dataframe 行-代码-timetag(多层索引)，列-字段
        """

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

    def get_market_data(self, market_data, stock_code=[], field=[], start="", end="", count=-1):
        """
        从dataframe解析数据成最终的数据格式，count　skip_paused都在在这里做
        :param market_data:
        :param stock_code:
        :param field:
        :param start:
        :param end:
        :param count:
        :return:
        """
        if start != "":
            start = data_transfer.date_str_to_int(start)
        else:
            start = 0
        if end != "":
            end = data_transfer.date_str_to_int(end)
        else:
            end = 0
        # （１）代码-1，字段-1，时间-1,  return float
        if len(stock_code) == 1 and len(field) == 1 and (start == end) and count == -1:
            return market_data[field[0]].ix[stock_code[0], end]
        # （２）代码-n，字段-1，时间-1,  return Series
        elif len(stock_code) > 1 and len(field) == 1 and (start == end) and count == -1:
            result_dict = {}
            for stock in stock_code:
                result_dict[stock] = market_data[field[0]].ix[stock, end]
            return pd.Series(result_dict)
        # （３）代码-1，字段-n，时间-1,  return Series
        elif len(stock_code) == 1 and len(field) > 1 and (start == end) and count == -1:
            result_dict = {}
            for field_one in field:
                result_dict[field_one] = market_data[field_one].ix[stock_code[0], end]
            return pd.Series(result_dict)
        # （４）代码-1，字段-1，时间-n,  return Series
        elif len(stock_code) == 1 and len(field) == 1 and (start != end) and count == -1:
            index = market_data[field[0]].ix[stock_code[0]].index
            index = index[index <= end]
            index = index[index >= start]
            return market_data[field[0]].ix[stock_code[0]][index]
        # （５）代码-n，字段-1，时间-n,  return dataframe 行-timetag，列-代码
        elif len(stock_code) > 1 and len(field) == 1 and (start != end) and count == -1:
            result_dict = {}
            for stock in stock_code:
                index = market_data.ix[stock].index
                index = index[index <= end]
                index = index[index >= start]
                result_dict[stock] = market_data[field[0]].ix[stock][index]
            return pd.DataFrame(result_dict)
        # （６）代码-n，字段-n，时间-1,  return dataframe 行-字段，列-代码
        elif len(stock_code) > 1 and len(field) > 1 and (start == end) and count == -1:
            result_dict = {}
            for stock in stock_code:
                result_dict[stock] = market_data.ix[stock].ix[end]
            return pd.DataFrame(result_dict).ix[field]
        # （７）代码-1，字段-n，时间-n,  return dataframe 行-timetag，列-字段
        elif len(stock_code) == 1 and len(field) > 1 and (start != end) and count == -1:
            index = market_data.ix[stock_code[0]].index
            index = index[index <= end]
            index = index[index >= start]
            return market_data.ix[stock_code[0]][field].ix[index]
        # 代码-n，字段-n，时间-n,  return dataframe 行-代码-timetag(多层索引)，列-字段
        else:
            result_dict = {}
            for stock in stock_code:
                index = market_data.ix[stock].index
                index = index[index <= end]
                index = index[index >= start]
                result_dict[stock] = market_data.ix[stock][field].ix[index]
            return pd.concat(result_dict, keys=stock_code)

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
    aa = GetData()
    daily_data = aa.get_all_market_data(stock_code=["000002.SZ", "000001.SH"],
                                        field=["open", "high", "low", "close", "volumn", "amount"],
                                        end="2018-01-02", period=Period.DAILY.value)
    # print(daily_data)
    data_1 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open"], start="2018-01-02",
                                end="2018-01-02", count=-1)
    # print(data_1)

    data_2 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open"], start="2018-01-02",
                                end="2018-01-02", count=-1)
    # print(data_2)

    data_3 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open", "high"], start="2018-01-02",
                                end="2018-01-02", count=-1)
    # print(data_3)
    data_4 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open"], start="2017-01-02",
                                end="2018-01-02", count=-1)
    # print(data_4)

    data_5 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open"], start="2017-01-02",
                                end="2018-01-02", count=-1)
    # print(data_5)

    data_6 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open", "high"],
                                start="2018-01-02", end="2018-01-02", count=-1)
    # print(data_6)

    data_7 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open", "high"], start="2017-01-02",
                                end="2018-01-02", count=-1)
    # print(data_7)
    data_8 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open", "high"],
                                start="2017-01-02",
                                end="2018-01-02", count=-1)
    print(data_8)
