# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : update_adj_factor.py 
# @Project : AmazingQuant 
# ------------------------------
import os
import time

import pandas as pd
import numpy as np
import tgw

from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_data import get_local_data
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor


class UpdateAdjFactor(object):
    def __init__(self):
        pass

    def get_backward_factor(self, code_sh_list, code_sz_list, calendar_index):
        backward_factor = pd.DataFrame(index=calendar_index)

        market = 'SH'
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            code_list = code_sh_list
            if market_type == tgw.MarketType.kSZSE:
                code_list = code_sz_list
                market = 'SZ'
            for code in code_list[:5]:
                print(code)
                adj_factor, _ = tgw.QueryExFactorTable(code)
                adj_factor.set_index(["ex_date"], inplace=True)
                adj_factor.sort_index(inplace=True)
                backward_factor[code] = adj_factor['cum_factor']
        # AdjustmentFactor.FROWARD_ADJ_FACTOR.value
        backward_factor.replace([np.inf, 0], np.nan, inplace=True)
        backward_factor.fillna(method='ffill', inplace=True)
        backward_factor.fillna(1, inplace=True)
        return backward_factor

    def cal_forward_factor(self, backward_factor):
        return backward_factor.div(backward_factor.iloc[-1])


if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    calendar_index = tgw_api_object.get_calendar()

    adj_factor_object = UpdateAdjFactor()
    backward_factor = adj_factor_object.get_backward_factor(code_sh_list, code_sz_list, calendar_index)
    folder_name = LocalDataFolderName.ADJ_FACTOR.value
    path = LocalDataPath.path + folder_name + '/'
    save_data_to_hdf5(path, AdjustmentFactor.FROWARD_ADJ_FACTOR.value, backward_factor)

