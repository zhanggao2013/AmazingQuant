# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/10/25
# @Author  : gao
# @File    : show_result.py 
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime

import pandas as pd

from pyecharts.charts import Bar, Line, Page
from pyecharts import options as opts
from pyecharts.components import Table

from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.analysis_center.net_value_analysis import NetValueAnalysis
from AmazingQuant.analysis_center.position_analysis import PositionAnalysis


class ShowResult(object):
    def __init__(self, net_analysis_result, position_analysis_result):
        self.net_analysis_result = net_analysis_result
        self.position_analysis_result = position_analysis_result

    def net_value(self):
        pass


if __name__ == '__main__':
    start_time = datetime(2018, 1, 2)
    end_time = datetime(2018, 12, 28)
    kline_object = GetKlineData()
    # 指数行情，沪深300代替
    all_index_data = kline_object.cache_all_index_data()
    benchmark_df = kline_object.get_market_data(all_index_data, stock_code=['000300.SH'], field=['close'], ) \
        .to_frame(name='close')
    net_value_df = pd.read_csv('account_data.csv', index_col=0)
    net_value_df.index = pd.DatetimeIndex(net_value_df.index)
    net_value_single_account_df = pd.DataFrame({})
    for i in net_value_df.groupby('account_id'):
        net_value_single_account_df = i[1]
        break
    net_value_analysis_obj = NetValueAnalysis(net_value_single_account_df, benchmark_df, start_time, end_time)
    net_analysis_result = net_value_analysis_obj.cal_net_analysis_result()

    position_data_df = pd.read_csv('position_data.csv', index_col=[0, 1], parse_dates=['time_tag'],
                                   dtype={'instrument': str})
    position_data_df = position_data_df[position_data_df.index.get_level_values(1) == 'test0']
    position_analysis_obj = PositionAnalysis(position_data_df)
    position_analysis_result = position_analysis_obj.cal_position_analysis_result()

    show_result_object = ShowResult(net_analysis_result, position_analysis_result)

    show_result_object.net_value()
