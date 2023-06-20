# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/20
# @Author  : gao
# @File    : update_finance_data.py 
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


class UpdateFinanceData(object):
    def __init__(self, code_list_hist):
        self.code_list_hist = code_list_hist

    def get_industry_class(self):
        for code in self.code_list_hist:
            task_id = tgw.GetTaskID()
            tgw.SetThirdInfoParam(task_id, "function_id", "A010010002")
            tgw.SetThirdInfoParam(task_id, "market_code", code)
            df, _ = tgw.QueryThirdInfo(task_id)

        return self.code_list_hist


if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    code_list_hist = tgw_api_object.get_code_list_hist()
    calendar_index = tgw_api_object.get_calendar()

    industry_class_df = None
    for code in code_list_hist[:20]:
        task_id = tgw.GetTaskID()
        tgw.SetThirdInfoParam(task_id, "function_id", "A010010002")
        tgw.SetThirdInfoParam(task_id, "market_code", code)
        df, _ = tgw.QueryThirdInfo(task_id)
        if industry_class_df is None:
            industry_class_df = df
        else:
            industry_class_df = industry_class_df.append(df)

    folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
    path = LocalDataPath.path + folder_name + '/'
    save_data_to_hdf5(path, folder_name, industry_class_df)
    a = get_local_data(path, folder_name + '.h5')
