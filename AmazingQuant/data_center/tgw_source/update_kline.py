# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : update_kline.py
# @Project : AmazingQuant
# ------------------------------
import os
import time

import pandas as pd
import tgw

from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor


class UpdateKlineData(object):
    def __init__(self):
        self.field = ['kline_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume_trade',
                      'value_trade']

    def get_kline_data(self, code_sh_list, code_sz_list, calendar):
        stock_kline = tgw.ReqKline()
        stock_kline.cq_flag = 0
        stock_kline.auto_complete = 1
        stock_kline.cyc_type = tgw.MDDatatype.kDayKline
        stock_kline.begin_date = 19900101
        stock_kline.end_date = 20991231
        stock_kline.begin_time = 930
        stock_kline.end_time = 1700
        num = 1
        # 获取深圳/上海股票的行情
        stock_data_dict = {}
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            stock_kline.market_type = tgw.MarketType.kSSE
            code_list = code_sh_list
            market = 'SH'
            if market_type == tgw.MarketType.kSZSE:
                stock_kline.market_type = tgw.MarketType.kSZSE
                code_list = code_sz_list
                market = 'SZ'

            for code in code_list:
                print(num, code)
                num += 1
                stock_kline.security_code = code
                stock_data_df, _ = tgw.QueryKline(stock_kline)
                stock_data_df = stock_data_df[self.field]
                stock_data_df.set_index(["kline_time"], inplace=True)
                stock_data_df = stock_data_df.reindex(calendar).fillna(method='ffill')
                stock_data_df[['open_price', 'high_price', 'low_price', 'close_price']] =\
                    stock_data_df[['open_price', 'high_price', 'low_price', 'close_price']] / 1000000
                stock_data_dict[code + '.' + market] = stock_data_df

        return stock_data_dict


if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    # code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    # calendar_index = tgw_api_object.get_calendar()
    #
    # kline_object = UpdateKlineData()
    # stock_data_dict = kline_object.get_kline_data(code_sh_list, code_sz_list, calendar_index)

    path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//' + LocalDataFolderName.KLINE_DAILY.value + \
           '//' + LocalDataFolderName.A_SHARE.value + '//'

    # field_data_dict = {}
    # for i in kline_object.field:
    #     if i != 'kline_time':
    #         field_data_pd = pd.DataFrame({key: value[i] for key, value in stock_data_dict.items()})
    #         field_data_dict[i] = field_data_pd
    #         field = ['kline_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume_trade', 'value_trade']
    #         save_data_to_hdf5(path, i, field_data_pd)
    open_df = get_local_data(path, 'open_price.h5')
    high_df = get_local_data(path, 'high_price.h5')
    low_df = get_local_data(path, 'low_price.h5')
    close_df = get_local_data(path, 'close_price.h5')
    volume_trade_df = get_local_data(path, 'volume_trade.h5')
    value_trade_df = get_local_data(path, 'value_trade.h5')

