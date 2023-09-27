# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/6/27
# @Author  : gao
# @File    : position_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
2 换手分析
（1）个数法换手率分析,衰减周期deley默认为5, 均值
    个数法,计算每期之间股票变动的数量并除以股票的总数量计算出的比率，例如t期买入[A,B,C,D,E]五只股票，t+1期买入[A,D,E,F,G]五只股票，那么这期间的换手率就是(2/5=40%)。
（2）权重法换手率分析,衰减周期deley默认为5, 均值
    权重法,不仅考虑股票本身的变化，还考虑了股票权重的变化。

3 持仓分析
（1）position_value_mean：股票市值均值-时序
（2）position_industry：行业市值-时序
（3）position_industry_pct:行业市值占比-时序
（4）position_industry_pct_mean：行业市值历史均值
"""
import time

import pandas as pd
import numpy as np

from AmazingQuant.data_center.api_data.get_index_class import GetIndexClass
from AmazingQuant.data_center.api_data.get_share import GetShare
from AmazingQuant.config.industry_class import sw_industry_one


class PositionAnalysis(object):
    def __init__(self, position_data_df):
        position_data_df['instrument_exchange'] = position_data_df['instrument'] + '.' + position_data_df['exchange']
        self.position_data_df = position_data_df.reset_index(level='account_id', drop=True)
        self.position_index = self.position_data_df.index.unique()
        columns = list(sw_industry_one.keys()) + ['other']
        # 行业市值-时序
        self.position_industry = pd.DataFrame(columns=columns)
        # 行业市值占比-时序
        self.position_industry_pct = pd.DataFrame(columns=columns)
        # 行业市值历史均值
        self.position_industry_pct_mean = None

        # 股票市值均值-时序
        self.position_value_mean = pd.DataFrame(columns=['value_mean'])

        # 个数法换手率turnover_num，衰减周期默认为5
        self.turnover_num_df = pd.DataFrame({})
        # 个数法换手率均值
        self.turnover_num_mean = None
        # 权重法换手率turnover_value，衰减周期默认为5
        self.turnover_value_df = pd.DataFrame({})
        # 权重法换手率均值
        self.turnover_value_mean = None

    def add_industry_share_value(self):
        """
        持仓数据增加字段
        industry 行业,
        share_value 股票的流通是指
        :return:
        """
        index_class_obj = GetIndexClass()
        index_class_obj.get_index_class()

        share_data_obj = GetShare()
        share_data = share_data_obj.get_share('float_a_share_value')

        def cal_industry_share_value(x, share_data):
            date_time = x.name
            stock_code = x['instrument_exchange']
            industry = index_class_obj.get_code_index_class_in_date(stock_code, date_time)
            share_value = share_data.loc[date_time, stock_code]
            return industry, share_value

        self.position_data_df['industry'], self.position_data_df['share_value'] = \
            zip(*self.position_data_df.apply(cal_industry_share_value, args=(share_data,), axis=1))

    def cal_industry_value(self):
        """
        持仓分析
            （1）position_value_mean：股票市值均值-时序, Dataframe, index:time_tag, column:value_mean
            （2）position_industry：行业市值-时序, Dataframe, index:time_tag, column:行业代码
            （3）position_industry_pct:行业市值占比-时序, Dataframe, index:time_tag, column:行业代码
            （4）position_industry_pct_mean：行业市值历史均值, Series, index:行业代码
        :return:
        """
        position_industry_list = []
        position_industry_pct_list = []
        position_value_mean_list = []
        for i in self.position_index:
            position_data_index = self.position_data_df.loc[i].copy()
            position_data_hold_value = position_data_index.groupby('industry').sum()['hold_value']
            position_data_hold_value.name = i
            position_industry_list.append(position_data_hold_value)
            total_value = position_data_hold_value.sum()
            position_industry_pct_list.append(100 * position_data_hold_value / total_value)

            position_stock_value_sum = pd.Series({'value_mean': position_data_index['hold_value'].sum()}, name=i)
            position_value_mean_list.append(position_stock_value_sum)

        self.position_industry = pd.concat(position_industry_list)
        self.position_industry_pct = pd.concat(position_industry_pct_list)
        self.position_value_mean = pd.concat(position_value_mean_list)
        self.position_industry = self.position_industry.fillna(0)
        self.position_industry_pct = self.position_industry_pct.fillna(0)
        self.position_industry_pct_mean = self.position_industry_pct.mean()

    def cal_turnover(self, delay=5):
        """
        换手分析
        个数法换手率, turnover_num_df，衰减周期默认为delay=5,DataFrame, index:time_tag, column:delay_1,delay_2, ... ,delay_n,
        个数法换手率均值, turnover_num_mean,  Series, index:delay_1,delay_2, ... ,delay_n,
        权重法换手率, turnover_value_df，衰减周期默认为5, DataFrame  , index:time_tag, column:delay_1,delay_2, ... ,delay_n,
        权重法换手率均值, turnover_value_mean, Series, index:delay_1,delay_2, ... ,delay_n,
        :param delay:
        :return:
        """
        turnover_num_list = []
        turnover_value_list = []
        for i in range(len(self.position_index) - delay):
            turnover_num_dict = {}
            turnover_value_dict = {}
            for delay_num in range(1, delay + 1, 1):
                position_stock_last = self.position_data_df.loc[self.position_index[i]]['instrument_exchange'].values
                position_data_index = self.position_data_df.loc[self.position_index[i + delay_num]]
                position_num = position_data_index.shape[0]
                position_stock = position_data_index['instrument_exchange'].values

                stock_change = np.setdiff1d(position_stock, position_stock_last)
                stock_change_num = stock_change.shape[0]
                turnover_num = 100 * stock_change_num / position_num
                turnover_num_dict['delay_' + str(delay_num)] = turnover_num

                stock_change_data = position_data_index[position_data_index['instrument_exchange'].isin(stock_change)]
                stock_change_value = stock_change_data['hold_value'].sum()
                turnover_value = 100 * stock_change_value / position_data_index['hold_value'].sum()
                turnover_value_dict['delay_' + str(delay_num)] = turnover_value
            # 个数法换手率turnover_num，衰减周期默认为5
            # self.turnover_num_df = self.turnover_num_df.append(pd.Series(turnover_num_dict,
            #                                                              name=self.position_index[i]))
            turnover_num_list.append(pd.Series(turnover_num_dict, name=self.position_index[i]))
            # 权重法换手率turnover_value，衰减周期默认为15
            # self.turnover_value_df = self.turnover_value_df.append(pd.Series(turnover_value_dict,
            #                                                                  name=self.position_index[i]))
            turnover_value_list.append(pd.Series(turnover_num_dict, name=self.position_index[i]))
        self.turnover_num_df = pd.concat(turnover_num_list, axis=1)
        self.turnover_value_df = pd.concat(turnover_value_list, axis=1)

        # 个数法换手率均值
        self.turnover_num_mean = self.turnover_num_df.mean()
        # 权重法换手率均值
        self.turnover_value_mean = self.turnover_value_df.mean()

    def cal_position_analysis_result(self):
        """
        持仓分析结果汇总
        :return:
        """
        self.add_industry_share_value()
        self.cal_industry_value()
        self.cal_turnover()
        position_analysis_result = {
            # 行业市值-时序
            'position_industry': self.position_industry,
            # 行业市值占比-时序
            'position_industry_pct': self.position_industry_pct,
            # 行业市值历史均值
            'position_industry_pct_mean': self.position_industry_pct_mean,
            # 股票市值均值-时序
            'position_value_mean': self.position_value_mean,
            # 个数法换手率turnover_num，衰减周期默认为5
            'turnover_num_df': self.turnover_num_df,
            # 个数法换手率均值
            'turnover_num_mean': self.turnover_num_mean,
            # 权重法换手率turnover_value，衰减周期默认为5
            'turnover_value_df': self.turnover_value_df,
            # 权重法换手率均值
            'turnover_value_mean': self.turnover_value_mean}
        return position_analysis_result


if __name__ == '__main__':
    position_data_df = pd.read_csv('position_data.csv', index_col=[0, 1], parse_dates=['time_tag'],
                                   dtype={'instrument': str})
    position_data_df = position_data_df[position_data_df.index.get_level_values(1) == 'test0']

    # position_data_df = position_data_df.iloc[:10000]

    position_analysis_obj = PositionAnalysis(position_data_df)
    # position_analysis_result = position_analysis_obj.cal_position_analysis_result()
