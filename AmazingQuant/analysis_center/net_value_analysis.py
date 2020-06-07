# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/16
# @Author  : gao
# @File    : net_value_analysis.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime

import pandas as pd

from AmazingQuant.data_center.api_data.get_kline import GetKlineData


class NetValueAnalysis(object):
    def __init__(self, net_value_df, benchmark_df, start_time, end_time):
        self.net_value_df = net_value_df.loc[start_time: end_time]
        self.benchmark_df = benchmark_df.loc[start_time: end_time]
        pass


if __name__ == '__main__':
    start_time = datetime(2010, 1, 4)
    end_time = datetime(2019, 11, 4)
    kline_object = GetKlineData()
    #
    # 指数行情，沪深300代替
    all_index_data = kline_object.cache_all_index_data()
    benchmark_df = kline_object.get_market_data(all_index_data, stock_code=['000300.SH'],
                                                field=['close'], start=start_time, end=end_time)
    # 策略精致，上证指数代替
    net_value_df = kline_object.get_market_data(all_index_data, stock_code=['000001.SH'],
                                                field=['close'], start=start_time, end=end_time)

    net_value_analysis_obj = NetValueAnalysis(net_value_df, benchmark_df, start_time, end_time)


