# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/19
# @Author  : gao
# @File    : cal_indicator.py
# @Project : AmazingQuant
# ------------------------------
import talib
import pandas as pd

from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_share import GetShare


class CalCondition(object):
    def __init__(self, open_df, high_df, low_df, close_df, volume_trade_df, value_trade_df, forward_factor):
        self.open_df = open_df
        self.high_df = high_df
        self.low_df = low_df
        self.close_df = close_df
        self.volume_trade_df = volume_trade_df
        self.value_trade_df = value_trade_df
        self.forward_factor = forward_factor

    def adj_data(self):
        """
        open_df, high_df, low_df, close_df, volume_trade_df，前复权
        value_trade_df 无需复权
        """
        self.open_df = self.open_df * self.forward_factor
        self.high_df = self.high_df * self.forward_factor
        self.low_df = self.low_df * self.forward_factor
        self.close_df = self.close_df * self.forward_factor
        self.volume_trade_df = self.volume_trade_df * self.forward_factor

    def cal_zhangfu(self):
        return self.close_df.pct_change()*100

    def cal_close_n_high(self, timeperiod=20):
        return self.close_df.fillna(0).apply(lambda x: talib.MAX(x, timeperiod=timeperiod))

    def cal_ma_value(self, timeperiod=30):
        return self.value_trade_df.apply(lambda x: talib.MA(x, timeperiod=timeperiod))

    def cal_turnover(self, share_data):
        return self.volume_trade_df.div(share_data)*100

    def condition1(self, timeperiod=10):
        """
        {条件1：前N1日 有涨停}
        N1:=20;
        ZHANGFU:=10;
        RESULT1:= IF(BARSLAST((CLOSE/REF(CLOSE,1)-1)*100>=ZHANGFU)<=N1,1,0);
        """
        zhangfu = self.cal_zhangfu()
        zhangting = zhangfu.applymap(lambda x: 1 if x>9.99 else 0)
        return zhangting.apply(lambda x: talib.MAX(x, timeperiod=timeperiod))

    def condition2(self, timeperiod=20):
        """
        {条件2：最新价小于前N2日最高价}
        N2:=20;
        HIGH_NUM:=HOD(CLOSE,N2);
        RESULT2:=IF(HIGH_NUM>1,1,0);
        """
        close_n_high = self.close_df < self.cal_close_n_high(timeperiod=timeperiod)
        close_n_high = close_n_high.replace(True, 1)
        close_n_high = close_n_high.replace(False, 0)
        return close_n_high

    def condition3(self, timeperiod=5, N1=20, M=2):
        """
        {条件3：MA5（VOL）与前N3日的MA5（VOL）比，大于M}
        N3:=20;
        M:=2;
        MA5_VOL:=MA(VOL,5);
        RESULT3:=IF(MA5_VOL/REF(MA5_VOL,N3)>M,1,0);
        """
        ma_value = self.cal_ma_value(timeperiod=timeperiod)
        ma_value_ratio = ma_value.pct_change(periods=N1)+1
        condition3 = ma_value_ratio > M
        condition3 = condition3.replace(True, 1)
        condition3 = condition3.replace(False, 0)
        return condition3


    def condition4(self, share_data, N=5):
        """
        {条件4：换手率大于N4}
        N4:=5;
        RESULT4:=IF(DYNAINFO(37)*100>N4,1,0);
        """
        turnover = self.cal_turnover(share_data)
        condition4 = turnover > N
        condition4 = condition4.replace(True, 1)
        condition4 = condition4.replace(False, 0)
        return condition4

    def cal_result(self, share_data):
        condition1 = self.condition1()
        condition2 = self.condition2()
        condition3 = self.condition3()
        condition4 = self.condition4(share_data)
        result = condition1 + condition2 + condition3 + condition4
        result = result > 3
        result = result.replace(True, 1)
        result = result.replace(False, 0)
        return result


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//' + LocalDataFolderName.KLINE_DAILY.value + \
           '//' + LocalDataFolderName.A_SHARE.value + '//'

    open_df = get_local_data(path, 'open.h5')
    high_df = get_local_data(path, 'high.h5')
    low_df = get_local_data(path, 'low.h5')
    close_df = get_local_data(path, 'close.h5')
    volume_trade_df = get_local_data(path, 'volume.h5')
    value_trade_df = get_local_data(path, 'amount.h5')

    adj_factor_path = LocalDataPath.path + LocalDataFolderName.ADJ_FACTOR.value + '/'
    forward_factor = get_local_data(adj_factor_path, AdjustmentFactor.FROWARD_ADJ_FACTOR.value + '.h5')

    cal_condition_object = CalCondition(open_df, high_df, low_df, close_df, volume_trade_df, value_trade_df,
                                        forward_factor)
    cal_condition_object.adj_data()

    share_data_obj = GetShare()
    share_data = share_data_obj.get_share('float_a_share')
    with Timer(True):
        factor_name = 'qiangshi'
        result_path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/' + factor_name + '/'
        result = cal_condition_object.cal_result(share_data).shift(1)
        save_data_to_hdf5(result_path, factor_name, result)
