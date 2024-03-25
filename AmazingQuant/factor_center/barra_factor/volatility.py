# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2024/1/7
# @Author  : gao
# @File    : volatility.py
# @Project : AmazingQuant
# ------------------------------
import datetime

import talib
import pandas as pd
import numpy as np

from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.data_center.api_data.get_share import GetShare
from AmazingQuant.data_center.api_data.get_kline import GetKlineData


class FactorVolatility(object):
    def __init__(self, start_date, end_date):
        self.close_df = None
        self.index_close_df = None
        self.start_date = start_date
        self.end_date = end_date

    def cache_data(self):
        kline_object = GetKlineData()
        all_market_data = kline_object.cache_all_stock_data(dividend_type=RightsAdjustment.FROWARD.value)
        self.close_df = all_market_data['close'].loc[self.start_date: self.end_date]

        all_index_data = kline_object.cache_all_index_data()
        self.index_close_df = all_index_data['close'].loc[self.start_date: self.end_date]

    def factor_beta(self, index_code='000300.SH'):
        # BETA（三级因子）:股票收益率对沪深300收益率进行时间序列回归，取回归系数，回归时间窗口为252个交易日，半衰期63个交易日。
        window, half_life = 252, 63
        L, Lambda = 0.5 ** (1 / half_life), 0.5 ** (1 / half_life)
        W = []
        for i in range(window):
            W.append(Lambda)
            Lambda *= L
        W = W[::-1]
        index_close_df = self.index_close_df[index_code]
        index_ratio_df = index_close_df.pct_change()*100
        index_ratio_df.dropna(inplace=True)
        ratio_df = self.close_df.pct_change()*100
        # ratio_df.dropna(axis=0, inplace=True)
        self.ratio_df  =ratio_df
        print(index_ratio_df, ratio_df)

        for i in range(ratio_df.shape[0]-window+1):
            tmp = ratio_df.iloc[i:i+window, :].copy()
            W_full = np.diag(W)
            Y_full = tmp.values

            X_full = np.c_[np.ones((window, 1)), index_ratio_df.iloc[i:i+window].values]
            print(Y_full.shape, X_full.shape)
            beta_full = np.linalg.pinv(X_full.T @ W_full @ X_full) @ X_full.T @ W_full @ Y_full
            # beta_full = pd.Series(beta_full[1], index=idx_full, name=tmp.index[-1])
            # weights = None

        # weights = (1. / share_data_in_date['float_a_share_value'])
        # weights[np.isinf(weights)] = 0
        # print('stock_return', stock_return, x, weights)
        # wls_model = sm.WLS(stock_return, x, weights=weights)


if __name__ == '__main__':
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)
    factor_volatility_object = FactorVolatility(start_date, end_date)
    factor_volatility_object.cache_data()
    factor_volatility_object.factor_beta()

    # share_data_obj = GetShare()
    # share_data = share_data_obj.get_share('float_a_share')
    # with Timer(True):
    #     dif, dea, macd = cal_factor_object.cal_macd()
    #     ema = cal_factor_object.cal_ema()
    #     k, d, j = cal_factor_object.cal_kdj()


