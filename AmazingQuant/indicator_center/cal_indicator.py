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
from AmazingQuant.data_center.api_data.get_share import GetShare


class CalIndicator(object):
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

    def cal_macd(self, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        输入为一个时间序列
        输出为多个时间序列
        """

        def macd(x):
            macd, macdsignal, macdhist = talib.MACD(x, fastperiod=fastperiod, slowperiod=slowperiod,
                                                    signalperiod=signalperiod)
            return [macd, macdsignal, macdhist]

        result = self.close_df.apply(lambda x: macd(x), result_type='expand')
        return pd.DataFrame(result.loc[0].T.to_dict()), pd.DataFrame(result.loc[1].T.to_dict()),\
            pd.DataFrame(result.loc[2].T.to_dict()).multiply(2)

    def cal_ema(self, timeperiod=30):
        """
        输入为一个时间序列
        输出为一个时间序列
        """
        return self.close_df.apply(lambda x: talib.EMA(x, timeperiod=timeperiod))

    def cal_kdj(self, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
        """
        输入为多个时间序列
        输出为多个时间序列
        """

        def kdj(x):
            slowk, slowd = talib.KDJ(self.high_df[x.name], self.low_df[x.name], x,
                                       fastk_period=fastk_period, slowk_period=slowk_period, slowk_matype=slowk_matype,
                                       slowd_period=slowd_period, slowd_matype=slowd_matype)
            slowj = 3 * slowk - 2 * slowd
            return [slowk, slowd, slowj]

        result = self.close_df.apply(lambda x: kdj(x), result_type='expand')
        return pd.DataFrame(result.loc[0].T.to_dict()), pd.DataFrame(result.loc[1].T.to_dict()), \
            pd.DataFrame(result.loc[2].T.to_dict())


if __name__ == '__main__':
    # tgw_login()

    # tgw_api_object = TgwApiData(20991231)
    # code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    # calendar_index = tgw_api_object.get_calendar()
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

    cal_indicator_object = CalIndicator(open_df, high_df, low_df, close_df, volume_trade_df, value_trade_df,
                                        forward_factor)
    cal_indicator_object.adj_data()

    share_data_obj = GetShare()
    share_data = share_data_obj.get_share('float_a_share')
    with Timer(True):
        # dif, dea, macd = cal_indicator_object.cal_macd()
        # ema = cal_indicator_object.cal_ema()
        # k, d, j = cal_indicator_object.cal_kdj()
        close_n_high = cal_indicator_object.cal_close_n_high()
        turnover = cal_indicator_object.cal_turnover(share_data)


