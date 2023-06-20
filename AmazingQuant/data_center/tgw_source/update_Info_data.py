# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/20
# @Author  : gao
# @File    : update_Info_data.py
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


class UpdateInfoData(object):
    def __init__(self, code_list_hist):
        self.code_list_hist = code_list_hist

    def get_data(self, id):
        result_df = None
        a = 1
        for code in self.code_list_hist:
            print(code, a)
            a += 1
            task_id = tgw.GetTaskID()
            tgw.SetThirdInfoParam(task_id, "function_id", id)
            tgw.SetThirdInfoParam(task_id, "market_code", code)
            tgw.SetThirdInfoParam(task_id, "start_date", "19900101")
            tgw.SetThirdInfoParam(task_id, "end_date", "20991231")
            if code in ['T00018.SH']:
                continue
            df, _ = tgw.QueryThirdInfo(task_id)
            if result_df is None:
                result_df = df
            else:
                result_df = result_df.append(df)
        return result_df

    def get_industry_class(self):
        """
        股本结构 A010010002
        """
        industry_class_df = self.get_data('A010010002')
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'industry_class', industry_class_df)

    def get_stock_struction(self):
        """
        股本结构 A010010004
        """
        stock_struction_df = self.get_data('A010010004')

        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'stock_struction', stock_struction_df)

    def get_finance_data(self):
        """
        A股一般企业资产负债表  A010050001
        A股一般企业利润表     A010050002
        A股一般企业现金流表   A010050003
        """
        data_dict = {"A010050001": "balance", "A010050002": "income", "A010050003": "cash_flow"}
        for key, value in data_dict.items():
            stock_struction_df = self.get_data(key)
            folder_name = LocalDataFolderName.FINANCE.value
            path = LocalDataPath.path + folder_name + '/'
            save_data_to_hdf5(path, value, stock_struction_df)

    def get_longhubang(self):
        """
        交易异动营业部买卖信息 A010070002
        """
        stock_struction_df = self.get_data('A010070002')

        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'longhubang', stock_struction_df)



if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    code_list_hist = tgw_api_object.get_code_list_hist()
    calendar_index = tgw_api_object.get_calendar()
    info_data_object = UpdateInfoData(code_list_hist)
    info_data_object.get_industry_class()
    info_data_object.get_stock_struction()
    info_data_object.get_finance_data()

    folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
    path = LocalDataPath.path + folder_name + '/'
    a = get_local_data(path, folder_name + '.h5')
