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
import tgw

from AmazingQuant.data_center.tgw_source.tgw_log import tgw_log
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.api_data.get_data import get_local_data


class UpdateAdjFactor(object):
    def __init__(self):
        pass

    def get_adj_factor(self, code_sh_list, code_sz_list):
        adj_factor = None
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            code_list = code_sh_list
            if market_type == tgw.MarketType.kSZSE:
                code_list = code_sz_list
            for code in code_list[:2]:
                adj_factor, _ = tgw.QueryExFactorTable(code)
                print(adj_factor)
        return adj_factor


if __name__ == '__main__':
    tgw_log()

    tgw_api_object = TgwApiData(20991231)
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    calendar_index = tgw_api_object.get_calendar()

    adj_factor_object = UpdateAdjFactor()
    adj_factor = adj_factor_object.get_adj_factor(code_sh_list, code_sz_list)

