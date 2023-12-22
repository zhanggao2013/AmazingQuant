# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/11/28
# @Author  : gao
# @File    : factor_analysis_report.py 
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime

from pyecharts.charts import Bar, Line, Page, Timeline
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts, InitOpts

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.data_center.api_data.get_kline import GetKlineData

from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.ic_analysis import IcAnalysis
from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.regression_analysis import RegressionAnalysis
from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.stratification_analysis import \
    StratificationAnalysis


class FactorAnalysis(object):
    def __init__(self, factor, factor_name, benchmark_code='000300.SH'):
        self.factor = factor
        self.factor_name = factor_name
        self.benchmark_code = benchmark_code

        self.stratification_analysis_obj = None
        self.regression_analysis_obj = None
        self.ic_analysis_obj = None

        kline_object = GetKlineData()
        market_data = kline_object.cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value, field=['close'])
        self.market_close_data = kline_object.get_market_data(market_data, field=['close'])

        # 指数行情，沪深300代替
        all_index_data = kline_object.cache_all_index_data()
        self.benchmark_df = kline_object.get_market_data(all_index_data, stock_code=[self.benchmark_code],
                                                         field=['close']).to_frame(name='close')

        # ic检测参数
        self.corr_method = 'spearmanr'
        self.ic_decay = 20

    def ic_analysis(self):
        """
        corr_method = {‘pearsonr’,:皮尔逊相关系数，非排名类因子
                    ‘spearmanr’:斯皮尔曼相关系数，排名类因子}
        """
        self.ic_analysis_obj = IcAnalysis(self.factor, self.factor_name, self.market_close_data, ic_decay=self.ic_decay)
        self.ic_analysis_obj.cal_ic_df(method=self.corr_method)
        self.ic_analysis_obj.cal_ic_indicator()
        self.ic_analysis_obj.save_ic_analysis_result(path, factor_name)
        return self.ic_analysis_obj

    def regression_analysis(self, wls_weight_method='float_value_inverse', nlags=10):
        """
        以流通市值平方根或者流通市值的倒数为权重做WLS（加权最小二乘法估计）,
        wls_weight_method = {‘float_value_inverse’：流通市值的倒数,
                             ‘float_value_square_root’：流通市值的倒数}

        nlags: 因子收益率的自相关系数acf和偏自相关系数pacf，的阶数
        """
        self.regression_analysis_obj = RegressionAnalysis(self.factor, self.factor_name,
                                                          self.market_close_data, self.benchmark_df)
        self.regression_analysis_obj.cal_factor_return(method=wls_weight_method)
        self.regression_analysis_obj.cal_t_value_statistics()
        self.regression_analysis_obj.cal_net_analysis()
        self.regression_analysis_obj.cal_acf(nlags=nlags)

        self.regression_analysis_obj.save_regression_analysis_result(path, factor_name)
        return self.regression_analysis_obj

    def stratification_analysis(self, group_num=5):
        """
        group_num，分组组数
        """
        self.stratification_analysis_obj = StratificationAnalysis(self.factor, self.factor_name, group_num=group_num)
        self.stratification_analysis_obj.group_analysis()
        return self.stratification_analysis_obj

    def table_factor_information(self):
        """
        因子评价的总体概要
        """
        date_list = list(self.factor.index.astype('str'))
        indicator_dict = {}
        indicator_dict["因子名称"] = self.factor_name
        indicator_dict["开始时间"] = min(date_list)
        indicator_dict["结束时间"] = max(date_list)
        table_factor_information = Table()
        headers = ["指标"]
        rows = [["数据"]]
        for key, value in indicator_dict.items():
            headers.append(key)
            rows[0].append(value)
        table_factor_information.add(headers, rows)
        table_factor_information.set_global_opts(title_opts=ComponentTitleOpts(title='因子评价的总体概要'))
        return table_factor_information

    # IC分析
    def table_ic_result(self):
        """
        ic_result
        """
        table_ic_result = Table()
        indicator_dict = {'ic_mean': 'IC均值', 'ic_std': 'IC标准差', 'ic_ir': 'IC_IR比率', 'ic_ratio': 'IC>0占比',
                          'ic_abs_ratio': '|IC|>0.02占比', 'ic_skewness': '偏度', 'ic_kurtosis': '峰度',
                          'ic_positive_ratio': '正相关显著比例', 'ic_negative_ratio': '负相关显著比例',
                          'ic_change_ratio': '状态切换比例', 'ic_unchange_ratio': '同向比例'}
        headers = ["衰减周期"] + [str(i + 1) + '日' for i in range(self.ic_decay)]
        rows = []
        ic_result = self.ic_analysis_obj.ic_result.applymap(lambda x: format(x, '.4f'))
        for key, value in indicator_dict.items():
            data = [value] + list(ic_result.loc[key, :])
            rows.append(data)
        table_ic_result.add(headers, rows)
        table_ic_result.set_global_opts(title_opts=ComponentTitleOpts(title='IC分析结果'))
        return table_ic_result

    def line_ic(self):
        """
        IC时序图
        """
        date_list = list(self.ic_analysis_obj.ic_df.index.astype('str'))
        selected_map_dict = {str(i+1)+'日': False for i in range(self.ic_decay) if 'delay_' + str(i+1) != 'delay_1'}
        line_ic = Bar() \
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=1, name="yAxis=1")])) \
            .set_global_opts(title_opts=opts.TitleOpts(title="IC时序图",
                                                       subtitle="衰减周期：" + str(self.ic_decay)),  # 标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 添加竖线信息
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100),
                             legend_opts=opts.LegendOpts(orient='vertical',
                                                         pos_bottom='bottom',
                                                         pos_top='top',
                                                         pos_left='right',
                                                         pos_right='right',
                                                         selected_map=selected_map_dict
                                                         ))  # 设置Y轴范围
        for i in range(self.ic_decay):
            ic_list = list(self.ic_analysis_obj.ic_df['delay_' + str(i + 1)].round(4))
            line_ic = line_ic \
                .add_xaxis(date_list) \
                .add_yaxis(str(i + 1) + "日", ic_list)

        return line_ic

    def line_ic_p_value(self):
        """
        IC检测时序图
        """
        date_list = list(self.ic_analysis_obj.p_value_df.index.astype('str'))
        selected_map_dict = {str(i+1)+'日': False for i in range(self.ic_decay) if 'delay_' + str(i+1) != 'delay_1'}
        line_ic_p_value = Bar() \
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=1, name="yAxis=1")])) \
            .set_global_opts(title_opts=opts.TitleOpts(title="IC检测P值时序图",
                                                       subtitle="衰减周期：" + str(self.ic_decay)),  # 标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 添加竖线信息
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100),
                             legend_opts=opts.LegendOpts(orient='vertical',
                                                         pos_bottom='bottom',
                                                         pos_top='top',
                                                         pos_left='right',
                                                         pos_right='right',
                                                         selected_map=selected_map_dict
                                                         ))  # 设置Y轴范围
        for i in range(self.ic_decay):
            ic_p_value_list = list(self.ic_analysis_obj.p_value_df['delay_' + str(i + 1)].round(4))
            line_ic_p_value = line_ic_p_value \
                .add_xaxis(date_list) \
                .add_yaxis(str(i + 1) + "日", ic_p_value_list)
        return line_ic_p_value

    # 回归分析
    def line_net_value(self):
        """
        收益
        net_value_df（净值曲线）
        benchmark_df（净值曲线）
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
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=1, name="yAxis=1")])) \
            .set_global_opts(title_opts=opts.TitleOpts(title="净值曲线",
                                                       subtitle="策略净值为：" + str(net_value_list[-1]) + "\n" +
                                                                "基准净值为：" + str(benchmark_list[-1])),  # 标题
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 添加竖线信息
                             yaxis_opts=opts.AxisOpts(min_=math.ceil(min(all_list) * 90) / 100,
                                                      max_=int(max(all_list) * 110) / 100),
                             datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100), )  # 设置Y轴范围
        return net_value_line

    def show_page(self, save_path_dir=''):
        page = Page(page_title='因子评价报告')

        table_factor_information = self.table_factor_information()

        page.add(table_factor_information)
        # table_ic_result = self.table_ic_result()
        # page.add(table_ic_result)
        #
        # line_ic = self.line_ic()
        # page.add(line_ic)
        #
        # line_ic_p_value = self.line_ic_p_value()
        # page.add(line_ic_p_value)

        page.render(save_path_dir + self.factor_name + "_因子评价报告.html")


if __name__ == '__main__':
    factor_name = 'factor_ma5'
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/' + factor_name + '/'
    factor_ma5 = get_local_data(path, factor_name + '_pre' + '.h5')

    factor_ma5 = factor_ma5[factor_ma5.index > datetime(2013, 2, 1)]
    factor_ma5 = factor_ma5[factor_ma5.index < datetime(2013, 4, 1)]
    # factor_ma5 = factor_ma5.iloc[:-50, :]

    factor_analysis_obj = FactorAnalysis(factor_ma5, factor_name)
    print('-' * 20, 'ic_analysis', '-' * 20)
    ic_analysis_obj = factor_analysis_obj.ic_analysis()
    print('-'*20, 'regression_analysis',  '-'*20)
    regression_analysis_obj = factor_analysis_obj.regression_analysis()
    # print('-'*20, 'stratification_analysis',  '-'*20)
    # stratification_analysis_obj = factor_analysis_obj.stratification_analysis()
    factor_analysis_obj.show_page(path)
