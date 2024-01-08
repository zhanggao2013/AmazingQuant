# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/16
# @Author  : gao
# @File    : trade_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
成交分析
"""
import pandas as pd


class TradeAnalysis(object):
    def __init__(self, trade_data_df, net_value_df):
        trade_data_df['instrument_exchange'] = trade_data_df['instrument'] + '.' + trade_data_df['exchange']
        self.trade_data_df = trade_data_df.reset_index(level='account_id', drop=True)
        self.trade_index = self.trade_data_df.index.unique()
        self.net_value_df = list(net_value_df.index.astype('str'))
        self.index_num = len(self.trade_index)
        # 交易股票总数量
        self.trade_stock_num = 0
        # 每日交易股票数量 - 时序
        self.trade_stock_num_day = {}
        # 平均日交易股票数量
        self.trade_stock_num_average = 0
        # 交易总金额
        self.trade_amount = 0
        # 每日交易金额 - 时序
        self.trade_amount_day = {}
        # 平均日交易额
        self.trade_amount_average = 0

        # 交易天数
        self.trade_day_num = 0
        # 交易天数占比
        self.trade_day_num_ratio = 0

        # 交易总次数
        self.trade_num_times = 0
        # 平均交易次数
        self.trade_num_times_average = 0
        # 每日交易次数-时序
        self.trade_num_times_day = {}
        # 开仓总次数
        self.open_num_times = 0
        # 平仓总次数
        self.close_num_times = 0
        # 平均买入次数
        self.open_num_times_average = 0
        # 平均卖出次数
        self.close_num_times_average = 0
        # 买入次数-时序
        self.open_num_times_day = {}
        # 卖出次数-时序
        self.close_num_times_day = {}

    def cal_trade_stock_amount(self):
        for i in self.trade_index:
            trade_data_index = self.trade_data_df.loc[i].copy()
            if isinstance(trade_data_index, pd.Series):
                trade_data_index = pd.DataFrame({i: trade_data_index}).T
                trade_data_index.index.name = 'time_tag'
            trade_stock_num = len(trade_data_index['instrument'].unique())
            # 交易股票总数量
            self.trade_stock_num += trade_stock_num
            # 每日交易股票数量 - 时序
            self.trade_stock_num_day[i] = trade_stock_num

            trade_amount = (trade_data_index['deal_volume'] * trade_data_index['order_price']).sum()
            # 交易总金额
            self.trade_amount += trade_amount
            # 每日交易金额 - 时序
            self.trade_amount_day[i] = trade_amount

        self.trade_stock_num_day = pd.Series(self.trade_stock_num_day)
        self.trade_amount_day = pd.Series(self.trade_amount_day)
        # 平均日交易股票数量
        self.trade_stock_num_average = round(self.trade_stock_num / self.index_num, 2)
        # 平均日交易额
        self.trade_amount_average = round(self.trade_amount / self.index_num, 2)

    def cal_trade_day_num(self):
        # 交易天数
        self.trade_day_num = len(set(self.trade_data_df.index.get_level_values(0)))
        # 交易天数占比
        self.trade_day_num_ratio = round(self.trade_day_num / self.index_num * 100, 2)

    def cal_trade_num_times(self):
        for i in self.trade_index:
            trade_data_index = self.trade_data_df.loc[i].copy()

            if isinstance(trade_data_index, pd.Series):
                trade_data_index = pd.DataFrame({i: trade_data_index}).T
                trade_data_index.index.name = 'time_tag'

            trade_num_times = trade_data_index.shape[0]
            # 交易总次数
            self.trade_num_times += trade_num_times
            # 每日交易次数
            self.trade_num_times_day[i] = trade_num_times

            open_data_index = trade_data_index[trade_data_index.offset == 'open']
            open_num_times = open_data_index.shape[0]
            close_data_index = trade_data_index[trade_data_index.offset == 'close']
            close_num_times = close_data_index.shape[0]
            # 开仓总次数
            self.open_num_times += open_num_times
            # 平仓总次数
            self.close_num_times += close_num_times
            # 买入次数-时序
            self.open_num_times_day[i] = open_num_times
            # 卖出次数-时序
            self.close_num_times_day[i] = close_num_times
        self.trade_num_times_day = pd.Series(self.trade_num_times_day)
        self.open_num_times_day = pd.Series(self.open_num_times_day)
        self.close_num_times_day = pd.Series(self.close_num_times_day)
        # 平均交易次数
        self.trade_num_times_average = round(self.trade_num_times / self.index_num, 2)
        # 平均买入次数
        self.open_num_times_average = round(self.open_num_times / self.index_num, 2)
        # 平均卖出次数
        self.close_num_times_average = round(self.close_num_times / self.index_num, 2)

    def cal_trade_analysis_result(self):
        """
        成交分析结果汇总
        :return:
        """
        self.cal_trade_stock_amount()
        self.cal_trade_day_num()
        self.cal_trade_num_times()
        trade_analysis_result = {
            # 交易股票总数量
            'trade_stock_num': self.trade_stock_num,
            # 每日交易股票数量 - 时序
            'trade_stock_num_day': self.trade_stock_num_day,
            # 平均日交易股票数量
            'trade_stock_num_average': self.trade_stock_num_average,
            # 交易总金额
            'trade_amount': self.trade_amount,
            # 每日交易金额 - 时序
            'trade_amount_day': self.trade_amount_day,
            # 平均日交易额
            'trade_amount_average': self.trade_amount_average,

            # 交易天数
            'trade_day_num': self.trade_day_num,
            # 交易天数占比
            'trade_day_num_ratio': self.trade_day_num_ratio,

            # 交易总次数
            'trade_num_times': self.trade_num_times,
            # 平均交易次数
            'trade_num_times_average': self.trade_num_times_average,
            # 每日交易次数
            'trade_num_times_day': self.trade_num_times_day,
            # 开仓总次数
            'open_num_times': self.open_num_times,
            # 平仓总次数
            'close_num_times': self.close_num_times,
            # 平均买入次数
            'open_num_times_average': self.open_num_times_average,
            # 平均卖出次数
            'close_num_times_average': self.close_num_times_average,
            # 买入次数-时序
            'open_num_times_day': self.open_num_times_day,
            # 卖出次数-时序
            'close_num_times_day': self.close_num_times_day,
        }
        return trade_analysis_result


if __name__ == '__main__':
    # 策略净值数据,index 为 datetime,取单个账户分析，后续可做多个账户
    net_value_df = pd.read_csv('account_data.csv', index_col=0)
    net_value_df.index = pd.DatetimeIndex(net_value_df.index)
    net_value_single_account_df = pd.DataFrame({})
    for i in net_value_df.groupby('account_id'):
        net_value_single_account_df = i[1]
        break

    trade_data_df = pd.read_csv('order_data.csv', index_col=[0, 1], parse_dates=['time_tag'],
                                dtype={'instrument': str})
    trade_data_df = trade_data_df[trade_data_df.index.get_level_values(1) == 'test0']
    # trade_data_obj = TradeAnalysis(trade_data_df, net_value_df)
    # trade_analysis_result = trade_data_obj.cal_trade_analysis_result()
