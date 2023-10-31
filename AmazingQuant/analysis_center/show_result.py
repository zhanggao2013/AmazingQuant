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
from pyecharts.options import ComponentTitleOpts

from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.analysis_center.net_value_analysis import NetValueAnalysis
from AmazingQuant.analysis_center.position_analysis import PositionAnalysis


class ShowResult(object):
    def __init__(self, net_analysis_result, position_analysis_result):
        self.net_analysis_result = net_analysis_result
        self.position_analysis_result = position_analysis_result

    def line_net_value(self):
        """
        收益
        net_value_df'（净值曲线）
        benchmark_df'（净值曲线）
        """
        net_value_list = list(self.net_analysis_result['net_value_df'].round(4)['net_value'])
        benchmark_list = list(self.net_analysis_result['benchmark_df'].round(4)['net_value'])
        all_list = net_value_list + benchmark_list
        net_value_line = Line() \
            .add_xaxis(list(self.net_analysis_result['net_value_df'].index.astype('str'))) \
            .add_yaxis("策略净值曲线", net_value_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')])) \
            .add_yaxis("基准净值曲线", benchmark_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')])) \
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.1)) \
            .set_global_opts(title_opts=opts.TitleOpts(title="净值曲线",
                                                       subtitle="策略净值为：" + str(net_value_list[-1]) + "\n" +
                                                                "基准净值为：" + str(benchmark_list[-1])),  # 标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 添加竖线信息
                             yaxis_opts=opts.AxisOpts(min_=math.ceil(min(all_list) * 90) / 100,
                                                      max_=int(max(all_list) * 110) / 100),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )  # 设置Y轴范围
        return net_value_line

    def table_net_value(self):
        """
        收益
        'net_year_yield'
        'benchmark_year_yield'
        'bull_win_index_ratio'
        'bear_win_index_ratio'
        'net_day_win_ratio'
        'benchmark_day_win_ratio'
        'net_day_ratio_average'
        'benchmark_day_ratio_average'
        'net_month_ratio_average'
        'benchmark_month_ratio_average'
        """
        indicator_dict = {'net_year_yield': "年化收益率",
                          'benchmark_year_yield': "基准年化收益率",
                          'bull_win_index_ratio': "牛市跑赢基准胜率",
                          'bear_win_index_ratio': "熊市跑赢基准胜率",
                          'net_day_win_ratio': "日胜率",
                          'benchmark_day_win_ratio': "基准日胜率",
                          'net_day_ratio_average': "日平均收益率",
                          'benchmark_day_ratio_average': "基准日平均收益率",
                          'net_month_ratio_average': "月平均收益率",
                          'benchmark_month_ratio_average': "基准月平均收益率", }
        table_net_value = Table()
        headers = ["指标"]
        rows = [["数据"]]
        for key, value in indicator_dict.items():
            headers.append(value)
            rows[0].append(round(self.net_analysis_result[key], 4))
        table_net_value.add(headers, rows)
        table_net_value.set_global_opts(title_opts=ComponentTitleOpts(title='收益分析'))
        return table_net_value

    def bar_day_profit_ratio(self):
        """
        收益率分布
        net_day_ratio_distribution'（柱状图）
        benchmark_day_ratio_distribution'（柱状图）
        net_month_ratio'（柱状图）
        benchmark_month_ratio'（柱状图）
        """
        net_day_ratio_distribution_list = list(self.net_analysis_result['net_day_ratio_distribution'].values())
        benchmark_day_ratio_distribution_list = list(
            self.net_analysis_result['benchmark_day_ratio_distribution'].values())
        bar_profit_ratio = Bar() \
            .add_xaxis(list(self.net_analysis_result['net_day_ratio_distribution'].keys())) \
            .add_yaxis("策略日收益率分布", [round(i, 4) for i in net_day_ratio_distribution_list],
                       ) \
            .add_yaxis("基准日收益率分布", [round(i, 4) for i in benchmark_day_ratio_distribution_list],
                       ) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))\
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="日收益率分布"), )


        return bar_profit_ratio

    def line_max_drawdown(self):
        """
        风险
        'net_value_df'（最大回撤曲线）
        'benchmark_df'（最大回撤）
        """
        drawdown_list = list(self.net_analysis_result['net_value_df'].round(4)['drawdown'])
        benchmark_drawdown_list = list(self.net_analysis_result['benchmark_df'].round(4)['drawdown'])
        net_max_drawdown = round(self.net_analysis_result['net_max_drawdown'], 4)
        benchmark_max_drawdown = round(self.net_analysis_result['benchmark_max_drawdown'], 4)
        max_drawdown_line = Line() \
            .add_xaxis(list(self.net_analysis_result['net_value_df'].index.astype('str'))) \
            .add_yaxis("策略最大回撤", drawdown_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min')])) \
            .add_yaxis("基准最大回撤", benchmark_drawdown_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min')])) \
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5)) \
            .set_global_opts(title_opts=opts.TitleOpts(title="最大回撤分析",
                                                       subtitle="策略历史最大回撤为：" + str(net_max_drawdown) + "\n" +
                                                                "基准历史最大回撤为：" + str(benchmark_max_drawdown)),
                             # 标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 添加竖线信息
                             yaxis_opts=opts.AxisOpts(
                                 min_=int(min(net_max_drawdown, benchmark_max_drawdown) * 110) / 100,
                                 max_=0),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )  # 设置Y轴范围
        return max_drawdown_line

    def table_risk(self):
        """
        风险
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
        """
        indicator_dict = {'net_year_volatility': "年化波动率",
                          'benchmark_year_volatility': "基准年化波动率",
                          'net_max_drawdown': "历史最大回撤",
                          'benchmark_max_drawdown': "基准历史最大回撤",
                          'net_day_volatility': "日收益率波动率",
                          'benchmark_day_volatility': "基准日收益率波动率",
                          'net_month_volatility': "月收益率波动率",
                          'benchmark_month_volatility': "基准月收益率波动率",
                          'downside_risk': "下行风险",
                          'net_skewness': "偏度",
                          'benchmark_skewness': "基准偏度",
                          'net_kurtosis': "峰度",
                          'benchmark_kurtosis': "基准峰度", }
        table_risk_value = Table()
        headers = ["指标"]
        rows = [["数据"]]
        for key, value in indicator_dict.items():
            headers.append(value)
            rows[0].append(round(self.net_analysis_result[key], 4))
        table_risk_value.add(headers, rows)
        table_risk_value.set_global_opts(title_opts=ComponentTitleOpts(title='风险分析'))
        return table_risk_value

    def table_profit_risk(self):
        """
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
        indicator_dict = {'beta': "beta",
                          'tracking_error': "跟踪误差",
                          'information_ratio': "信息比率",
                          'alpha': "alpha",
                          'sharpe': "夏普比率",
                          'sortino_ratio': "索提诺比率",
                          'treynor_ratio': "特雷诺比率",
                          'calmar_ratio': "卡玛比率", }
        table_profit_risk_value = Table()
        headers = ["指标"]
        rows = [["数据"]]
        for key, value in indicator_dict.items():
            headers.append(value)
            rows[0].append(round(self.net_analysis_result[key], 4))
        table_profit_risk_value.add(headers, rows)
        table_profit_risk_value.set_global_opts(title_opts=ComponentTitleOpts(title='收益风险比分析'))
        return table_profit_risk_value

    def show_page(self, save_path_dir=''):
        page = Page()

        net_value_line = self.line_net_value()
        page.add(net_value_line)

        table_net_value = self.table_net_value()
        page.add(table_net_value)

        bar_profit_ratio = self.bar_day_profit_ratio()
        page.add(bar_profit_ratio)

        max_drawdown_line = self.line_max_drawdown()
        page.add(max_drawdown_line)

        table_risk_value = self.table_risk()
        page.add(table_risk_value)

        table_profit_risk_value = self.table_profit_risk()
        page.add(table_profit_risk_value)

        page.render(save_path_dir + "回测绩效分析报告.html")


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
