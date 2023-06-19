# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/19
# @Author  : gao
# @File    : cal_indicator.py 
# @Project : AmazingQuant 
# ------------------------------
import pandas as pd
import numpy as np
import tgw


from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor






if __name__ == '__main__':

    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    calendar_index = tgw_api_object.get_calendar()
    path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//'+LocalDataFolderName.KLINE_DAILY.value + \
        '//' + LocalDataFolderName.A_SHARE.value + '//'

    open_df = get_local_data(path, 'open_price.h5')
    high_df = get_local_data(path, 'high_price.h5')
    low_df = get_local_data(path, 'low_price.h5')
    close_df = get_local_data(path, 'close_price.h5')
    volume_trade_df = get_local_data(path, 'volume_trade.h5')
    value_trade_df = get_local_data(path, 'value_trade.h5')

    adj_factor_path = LocalDataPath.path + LocalDataFolderName.ADJ_FACTOR.value + '/'
    forward_factor = get_local_data(adj_factor_path, AdjustmentFactor.FROWARD_ADJ_FACTOR.value+'.h5')

    a = forward_factor * close_df
