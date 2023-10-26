# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/10/25
# @Author  : gao
# @File    : show_result.py 
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime
import math

import pandas as pd

from pyecharts.charts import Bar, Line, Page
from pyecharts import options as opts
from pyecharts.components import Table

from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.analysis_center.net_value_analysis import NetValueAnalysis
from AmazingQuant.analysis_center.position_analysis import PositionAnalysis


class ShowResult(object):
    """
    收益
    'net_value_df'（净值曲线）
    'benchmark_df'（净值曲线）
    'net_year_yield'
    'benchmark_year_yield'
    'bull_win_index_ratio'
    'bear_win_index_ratio'
    'net_day_win_ratio'
    'benchmark_day_win_ratio'
    'net_day_ratio_distribution'（柱状图）
    'benchmark_day_ratio_distribution'（柱状图）
    'net_day_ratio_average'
    'benchmark_day_ratio_average'
    'net_month_ratio'（柱状图）
    'benchmark_month_ratio'（柱状图）
    'net_month_ratio_average'
    'benchmark_month_ratio_average'

    风险
    'net_value_df'（最大回撤曲线）
    'benchmark_df'（最大回撤）
    'net_year_volatility'
    'benchmark_year_volatility'
    'net_max_drawdown'
    'benchmark_max_drawdown'
    'net_day_volatility'
    'benchmark_day_volatility'
    'net_month_volatility'
    'benchmark_month_volatility'
    'downside_risk'
    'net_skewness'
    'net_kurtosis'
    'benchmark_skewness'
    'benchmark_kurtosis'

    收益风险比
    'beta'
    'tracking_error'
    'information_ratio'
    'alpha'
    'sharpe'
    'sortino_ratio'
    'treynor_ratio'
    'calmar_ratio'
    """

    def __init__(self, net_analysis_result, position_analysis_result):
        self.net_analysis_result = net_analysis_result
        self.position_analysis_result = position_analysis_result

    def profit_net_value(self):
        net_value_list = list(self.net_analysis_result['net_value_df'].round(4)['net_value'])
        benchmark_list = list(self.net_analysis_result['benchmark_df'].round(4)['net_value'])
        all_list = net_value_list+benchmark_list
        net_value_line = Line()\
            .add_xaxis(list(self.net_analysis_result['net_value_df'].index.astype('str'))) \
            .add_yaxis("策略净值曲线", net_value_list) \
            .add_yaxis("基准净值曲线", benchmark_list)\
            .set_global_opts(title_opts=opts.TitleOpts(title="净值曲线"), #标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),#添加竖线信息
                             yaxis_opts=opts.AxisOpts(min_=math.ceil(min(all_list)*90)/100,
                                                      max_=int(max(all_list)*110)/100),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100),)  # 设置Y轴范围
        return net_value_line

    def show_page(self):
        page = Page()
        net_value_line = self.profit_net_value()
        page.add(net_value_line)
        page.render("回测绩效分析报告.html")


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

    show_result_object.show_page()
