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

from pyecharts.charts import Bar, Line, Page, Timeline
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.analysis_center.net_value_analysis import NetValueAnalysis
from AmazingQuant.analysis_center.position_analysis import PositionAnalysis
from AmazingQuant.config.industry_class import sw_industry_one


class ShowResult(object):
    def __init__(self, net_analysis_result, position_analysis_result):
        self.net_analysis_result = net_analysis_result
        self.position_analysis_result = position_analysis_result

    # 净值分析
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
        日收益率分布
        net_day_ratio_distribution'（柱状图）
        benchmark_day_ratio_distribution'（柱状图）
        """
        net_day_ratio_distribution_list = list(self.net_analysis_result['net_day_ratio_distribution'].values())
        benchmark_day_ratio_distribution_list = list(
            self.net_analysis_result['benchmark_day_ratio_distribution'].values())
        bar_profit_ratio_day = Bar() \
            .add_xaxis(list(self.net_analysis_result['net_day_ratio_distribution'].keys())) \
            .add_yaxis("策略日收益率分布", [round(i, 4) for i in net_day_ratio_distribution_list],
                       ) \
            .add_yaxis("基准日收益率分布", [round(i, 4) for i in benchmark_day_ratio_distribution_list],
                       ) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="日收益率分布"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )
        return bar_profit_ratio_day

    def bar_month_profit_ratio(self):
        """
        月度收益率
        net_month_ratio'（柱状图）
        benchmark_month_ratio'（柱状图）
        """
        net_month_ratio_distribution_list = list(self.net_analysis_result['net_month_ratio'].values())
        benchmark_month_ratio_distribution_list = list(
            self.net_analysis_result['benchmark_month_ratio'].values())
        bar_profit_ratio_month = Bar() \
            .add_xaxis(list(self.net_analysis_result['net_month_ratio'].keys())) \
            .add_yaxis("策略月收益率", [round(i, 4) for i in net_month_ratio_distribution_list],
                       ) \
            .add_yaxis("基准月收益率", [round(i, 4) for i in benchmark_month_ratio_distribution_list],
                       ) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="月收益率"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )

        return bar_profit_ratio_month

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

    # 持仓分析
    def bar_position_value_mean(self):
        """
        'position_value_mean'：股票持仓市值-时序, Series, index:time_tag
        """
        position_value_mean = list(self.position_analysis_result['position_value_mean'])
        bar_position_value_mean = Bar() \
            .add_xaxis(list(self.position_analysis_result['position_value_mean'].index.astype('str'))) \
            .add_yaxis("股票持仓市值（万）", [round(i / 10000, 4) for i in position_value_mean]) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="股票持仓市值"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80), )

        return bar_position_value_mean

    def bar_position_industry_pct(self):
        """
        'position_industry_pct',行业市值占比-时序, Dataframe, index:time_tag, column:行业代码
        """

        def get_industry_value(industry=None):
            position_industry_pct = list(self.position_analysis_result['position_industry_pct'][industry].values)
            position_industry_pct = [round(i, 4) for i in position_industry_pct]
            title = sw_industry_one[industry] + "（%）"

            bar_industry_value_pct = Bar() \
                .add_xaxis(xaxis_data=list(self.position_analysis_result['position_industry_pct'].index.astype('str'))) \
                .add_yaxis('行业市值占比', position_industry_pct) \
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
                .set_global_opts(title_opts=opts.TitleOpts(title="股票持仓行业市值占比", subtitle=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                                 yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                                          min_=min(position_industry_pct),
                                                          max_=max(position_industry_pct)),
                                 datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80),
                                 tooltip_opts=opts.TooltipOpts(trigger="axis"),
                                 )  # 添加竖线信息

            return bar_industry_value_pct

        # 生成时间轴的图
        timeline_position_industry_pct = Timeline()

        for industry in sw_industry_one:
            timeline_position_industry_pct.add(get_industry_value(industry), time_point=sw_industry_one[industry])

        # 1.0.0 版本的 add_schema 暂时没有补上 return self 所以只能这么写着
        timeline_position_industry_pct.add_schema(pos_bottom='-5px', pos_top='top', pos_left='left', pos_right='left',
                                                  orient='vertical',
                                                  play_interval=0)
        return timeline_position_industry_pct

    def line_position_industry(self):
        """
        'position_industry',行业市值-时序, Dataframe, index:time_tag, column:行业代码
        """

        def get_industry_value(industry=None):
            position_industry = list(self.position_analysis_result['position_industry'][industry].values)
            position_industry = [round(i / 10000, 4) for i in position_industry]
            title = sw_industry_one[industry] + "（万）"

            line_industry_value = Line() \
                .add_xaxis(xaxis_data=list(self.position_analysis_result['position_industry'].index.astype('str'))) \
                .add_yaxis('行业市值', position_industry) \
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
                .set_global_opts(title_opts=opts.TitleOpts(title="股票持仓行业市值", subtitle=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                                 yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                                          min_=min(position_industry),
                                                          max_=max(position_industry)),
                                 datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80),
                                 tooltip_opts=opts.TooltipOpts(trigger="axis"), )  # 添加竖线信息
            return line_industry_value

        # 生成时间轴的图
        timeline_position_industry = Timeline()

        for industry in sw_industry_one:
            timeline_position_industry.add(get_industry_value(industry), time_point=sw_industry_one[industry])

        # 1.0.0 版本的 add_schema 暂时没有补上 return self 所以只能这么写着
        timeline_position_industry.add_schema(pos_bottom='-5px', pos_top='top', pos_left='left', pos_right='left',
                                              orient='vertical',
                                              play_interval=0)
        return timeline_position_industry

    def bar_position_industry_pct_mean(self):
        """
        'position_industry_pct_mean',行业市值历史占比均值, Series, index:行业代码
        """
        position_value_mean = list(self.position_analysis_result['position_industry_pct_mean'])
        position_value_mean_xaxis = list(
            self.position_analysis_result['position_industry_pct_mean'].index.astype('str'))
        position_value_mean_xaxis = [sw_industry_one[i] for i in position_value_mean_xaxis]
        bar_position_industry_pct_mean = Bar() \
            .add_xaxis(position_value_mean_xaxis) \
            .add_yaxis("行业市值历史占比均值（%）", [round(i, 4) for i in position_value_mean]) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="行业市值历史占比均值"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80), )

        return bar_position_industry_pct_mean

    def bar_turnover_num(self, delay=5):
        """
        个数法换手率, turnover_num_df，衰减周期默认为delay=5,DataFrame, index:time_tag, column:delay_1,delay_2, ... ,delay_n,
        权重法换手率, turnover_value_df，衰减周期默认为5, DataFrame  , index:time_tag, column:delay_1,delay_2, ... ,delay_n,
        """
        def get_turnover_num(delay):
            turnover_num_list = list(self.position_analysis_result['turnover_num_df'].loc[delay, :].values)
            turnover_num_list = [round(i, 2) for i in turnover_num_list]

            turnover_value_list = list(self.position_analysis_result['turnover_value_df'].loc[delay, :].values)
            turnover_value_list = [round(i, 2) for i in turnover_value_list]

            bar_turnover_num = Bar() \
                .add_xaxis(xaxis_data=list(self.position_analysis_result['turnover_num_df'].columns.astype('str'))) \
                .add_yaxis('个数法', turnover_num_list) \
                .add_yaxis('权重法', turnover_value_list) \
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
                .set_global_opts(title_opts=opts.TitleOpts(title="换手率（%）"),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                                 yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                                          min_=min(turnover_num_list),
                                                          max_=max(turnover_num_list)),
                                 datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80),
                                 tooltip_opts=opts.TooltipOpts(trigger="axis"),
                                 )  # 添加竖线信息
            return bar_turnover_num

        # 生成时间轴的图
        timeline_turnover_num = Timeline()

        for delay in self.position_analysis_result['turnover_num_df'].index:
            timeline_turnover_num.add(get_turnover_num(delay), time_point=delay)

        timeline_turnover_num.add_schema(pos_bottom='-5px', pos_top='top', pos_left='left', pos_right='left',
                                         orient='vertical', play_interval=0)
        return timeline_turnover_num

    def bar_turnover_num_mean(self):
        """
        个数法换手率均值, turnover_num_mean,  Series, index:delay_1,delay_2, ... ,delay_n,
        权重法换手率均值, turnover_value_mean, Series, index:delay_1,delay_2, ... ,delay_n,
        """
        turnover_num_mean = list(self.position_analysis_result['turnover_num_mean'].values)
        turnover_num_mean = [round(i, 2) for i in turnover_num_mean]

        turnover_value_mean = list(self.position_analysis_result['turnover_value_mean'].values)
        turnover_value_mean = [round(i, 2) for i in turnover_value_mean]

        bar_turnover_num_mean = Bar() \
            .add_xaxis(list(self.position_analysis_result['turnover_num_mean'].index.astype('str'))) \
            .add_yaxis("个数法（%）", turnover_num_mean) \
            .add_yaxis("权重法（%）", turnover_value_mean) \
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             title_opts=opts.TitleOpts(title="换手率均值（%）"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )
        return bar_turnover_num_mean

    def show_page(self, save_path_dir=''):
        page = Page()

        net_value_line = self.line_net_value()
        page.add(net_value_line)

        table_net_value = self.table_net_value()
        page.add(table_net_value)

        bar_profit_ratio_day = self.bar_day_profit_ratio()
        page.add(bar_profit_ratio_day)

        bar_profit_ratio_month = self.bar_month_profit_ratio()
        page.add(bar_profit_ratio_month)

        max_drawdown_line = self.line_max_drawdown()
        page.add(max_drawdown_line)

        table_risk_value = self.table_risk()
        page.add(table_risk_value)

        table_profit_risk_value = self.table_profit_risk()
        page.add(table_profit_risk_value)

        bar_position_value_mean = self.bar_position_value_mean()
        page.add(bar_position_value_mean)

        bar_position_industry_pct = self.bar_position_industry_pct()
        page.add(bar_position_industry_pct)

        timeline_position_industry = self.line_position_industry()
        page.add(timeline_position_industry)

        bar_position_industry_pct_mean = self.bar_position_industry_pct_mean()
        page.add(bar_position_industry_pct_mean)

        timeline_turnover_num = self.bar_turnover_num()
        page.add(timeline_turnover_num)

        bar_turnover_num_mean = self.bar_turnover_num_mean()
        page.add(bar_turnover_num_mean)

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
