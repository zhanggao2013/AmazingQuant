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
        复权因子和skip_pause在这做
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
                self.conn.check_connected()
                stock_market_data = self.conn.select_colum(db_name=db_name, table=stock,
                                                           value={"timetag": {"$lte": end}},
                                                           colum=colum)
                stock_market_data_list = list(stock_market_data)
                if stock_market_data_list:
                    df = pd.DataFrame(stock_market_data_list)
                    values.append(pd.DataFrame(df[field].values, index=df['timetag'], columns=field))
            market_data = pd.concat(values, keys=stock_code)
        elif period == Period.ONE_MIN.value:
            db_name = DatabaseName.MARKET_DATA_ONE_MIN.value

        return market_data

    def get_market_data(self, market_data, stock_code=[], field=[], start="", end="", count=-1):
        """
        从dataframe解析数据成最终的数据格式，count都在在这里做
        因为停牌或者其他原因取不到数据的，１　２　３　返回的是－１，其他返回的是pandas的空或者NaN，所以可以使用　＞０判断是否取到值
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
            try:
                return market_data[field[0]].ix[stock_code[0], end]
            # 停牌或者其他情情况取不到数据的返回-1
            except:
                return -1
        # （２）代码-n，字段-1，时间-1,  return Series
        elif len(stock_code) > 1 and len(field) == 1 and (start == end) and count == -1:
            result_dict = {}
            for stock in stock_code:
                try:
                    result_dict[stock] = market_data[field[0]].ix[stock, end]
                except:
                    result_dict[stock] = -1
            return pd.Series(result_dict)
        # （３）代码-1，字段-n，时间-1,  return Series
        elif len(stock_code) == 1 and len(field) > 1 and (start == end) and count == -1:
            result_dict = {}
            for field_one in field:
                try:
                    result_dict[field_one] = market_data[field_one].ix[stock_code[0], end]
                except:
                    result_dict[field_one] = -1
            return pd.Series(result_dict)
        # （４）代码-1，字段-1，时间-n,  return Series
        elif len(stock_code) == 1 and len(field) == 1 and (start != end) and count == -1:
            try:
                series = market_data[field[0]].ix[stock_code[0]]
            except KeyError:
                return pd.Series()

            series = series[series.index >= start]
            series = series[series.index <= end]
            return series
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
                try:
                    result_dict[stock] = market_data.ix[stock].ix[end]
                except:
                    result_dict[stock] = pd.Series()
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

    def get_end_timetag(self, benchmark, period=Period.DAILY.value):
        if period == Period.DAILY.value:
            db_name = DatabaseName.MARKET_DATA_DAILY.value
        elif period == Period.ONE_MIN.value:
            db_name = DatabaseName.MARKET_DATA_ONE_MIN.value
        colum = {"_id": 0, "timetag": 1}
        end_timetag_list = self.conn.select_colum(db_name=db_name, table=benchmark,
                                                  value={},
                                                  colum=colum)
        end_timetag = str(int(max([i["timetag"] for i in list(end_timetag_list)])))
        return end_timetag[:4] + "-" + end_timetag[4:6] + "-" + end_timetag[6:]


if __name__ == "__main__":
    aa = GetData()
    stock_list = ['000300.SH', '601857.SH', '601866.SH', '601872.SH', '601877.SH', '601878.SH', '601881.SH', '601888.SH']
    daily_data = aa.get_all_market_data(stock_code=stock_list, field=["open", "high", "low", "close", "volumn", "amount"],
                                                end="2015-03-12", period=Period.DAILY.value)
    print(daily_data)
    # print(daily_data)
    # data_1 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open"], start="2018-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_1)
    #
    # data_2 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open"], start="2018-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_2)
    #
    # data_3 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open", "high"], start="2018-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_3)
    # data_4 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open"], start="2017-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_4)
    #
    # data_5 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open"], start="2017-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_5)
    #
    # data_6 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open", "high"],
    #                             start="2019-01-02", end="2019-01-02", count=-1)
    # # print(data_6)
    #
    # data_7 = aa.get_market_data(daily_data, stock_code=["000002.SZ"], field=["open", "high"], start="2017-01-02",
    #                             end="2018-01-02", count=-1)
    # # print(data_7)
    # data_8 = aa.get_market_data(daily_data, stock_code=["000002.SZ", "000001.SH"], field=["open", "high"],
    #                             start="2017-01-02",
    #                             end="2018-01-02", count=-1)
    # #print(data_8)
