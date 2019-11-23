# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/23
# @Author  : gao
# @File    : save_a_share_adj_factor.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd
import numpy as np

from AmazingQuant.data_center.database_field.field_a_share_ex_right_dividend import AShareExRightDividend
from AmazingQuant.data_center.database_field.field_a_share_kline import Kline
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class SaveAShareAdjFactor(object):
    def __init__(self, data_path, field_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.field_is_str_list = get_field_str_list(field_path)

    def save_a_share_adj_factor(self):
        """
        取当日收盘价，作为转、送的股价，
        再计算复权因子更新到AShareExRightDividend, 复权因子adj_factor
        :return:
        """
        database = 'stock_base_data'
        with MongoConnect(database):
            pass


if __name__ == '__main__':
    save_cash_flow_obj = SaveAShareAdjFactor(data_path, field_path)
    save_cash_flow_obj.save_a_share_adj_factor()
