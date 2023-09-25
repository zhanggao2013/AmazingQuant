# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : download_kline.py
# @Project : AmazingQuant
# ------------------------------
import os
import time
import datetime

import pandas as pd
import tgw

from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor
from AmazingQuant.utils.data_transfer import date_to_datetime, datetime_to_int


class DownloadKlineData(object):
    def __init__(self, path):
        # 原始字段名
        self.field = ['open_price', 'high_price', 'low_price', 'close_price', 'volume_trade', 'value_trade']
        # 本地落库字段名
        self.field_dict = {'open_price': 'open', 'high_price': 'high', 'low_price': 'low',
                            'close_price': 'close', 'volume_trade': 'volume', 'value_trade': 'amount'}
        self.path = path

    def download_kline_data(self, code_sh_list, code_sz_list, calendar):
        # 取数据的入参，和返回值都为int，这里把交易日列表修改为int型
        calendar_int = [datetime_to_int(i) for i in calendar]
        # 股票代码上交所加后缀'.SH'，深交所加后缀'.SZ'
        code_market_list = []
        for code in code_sh_list:
            code_market_list.append(code + '.SH')
        for code in code_sz_list:
            code_market_list.append(code + '.SZ')

        download_begin_date = datetime.datetime(1990, 1, 1)
        local_data = {}
        try:
            date_list = []
            for i in self.field_dict.values():
                local_data[i] = get_local_data(self.path, i+'.h5').reindex(columns=code_market_list)
                date_list.append(max(local_data[i].index))
            date_list_min = min(date_list)
            download_begin_date = calendar[calendar.index(date_list_min) - 1]
            end_date = calendar[calendar.index(date_list_min) - 2]
            print('download_begin_date', download_begin_date)
            print('end_date', end_date)
            for i in self.field_dict.values():
                local_data[i] = local_data[i].loc[:end_date, :]
        except FileNotFoundError:
            for i in self.field_dict.values():
                local_data[i] = pd.DataFrame({})
            print('File does not exist')
        print('download_begin_date', download_begin_date)
        stock_kline = tgw.ReqKline()
        stock_kline.cq_flag = 0
        stock_kline.auto_complete = 1
        stock_kline.cyc_type = tgw.MDDatatype.kDayKline
        # stock_kline.cyc_type = tgw.MDDatatype.k1KLine
        stock_kline.begin_date = datetime_to_int(download_begin_date)
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
                stock_data_df, error = tgw.QueryKline(stock_kline)
                # print(stock_data_df, error, stock_data_df.empty)
                if error == "" and not stock_data_df.empty:
                    stock_data_df.set_index(["kline_time"], inplace=True)
                    stock_data_df = stock_data_df[self.field]
                    # print(code, stock_data_df)
                    stock_data_df = stock_data_df.reindex(calendar_int).fillna(method='ffill')
                    # stock_data_df = stock_data_df.loc[:20230815, :]
                    stock_data_df[['open_price', 'high_price', 'low_price', 'close_price']] =\
                        stock_data_df[['open_price', 'high_price', 'low_price', 'close_price']] / 1000000
                    stock_data_dict[code + '.' + market] = stock_data_df
        field_data_dict = {}
        for i in self.field:
            field_data_pd = pd.DataFrame({key: value[i] for key, value in stock_data_dict.items()})
            field_data_pd.index = pd.Series([date_to_datetime(str(i)) for i in field_data_pd.index])
            field_data_dict[self.field_dict[i]] = field_data_pd
            if download_begin_date != datetime.datetime(1990, 1, 1):
                field_data_dict[self.field_dict[i]] = pd.concat([local_data[self.field_dict[i]],
                                                                 field_data_pd.loc[download_begin_date:, :]])
            save_data_to_hdf5(self.path, self.field_dict[i], field_data_dict[self.field_dict[i]])
            print('save_data_to_hdf5', self.field_dict[i])
        return field_data_dict


if __name__ == '__main__':
    tgw_login(server_mode=True)

    tgw_api_object = TgwApiData(20991231)
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    index_code_sh_list, index_code_sz_list = tgw_api_object.get_code_list(index = True)
    
    calendar_index = tgw_api_object.get_calendar(data_type='datetime')
    path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//' + LocalDataFolderName.KLINE_DAILY.value + \
           '//' + LocalDataFolderName.A_SHARE.value + '//'

    kline_object = DownloadKlineData(path)
    field_data_dict = kline_object.download_kline_data(code_sh_list, code_sz_list, calendar_index)
    
    path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//' + LocalDataFolderName.KLINE_DAILY.value + \
           '//' + LocalDataFolderName.INDEX.value + '//'
    kline_object = DownloadKlineData(path)

    field_data_dict = kline_object.download_kline_data(index_code_sh_list, index_code_sz_list, calendar_index)

