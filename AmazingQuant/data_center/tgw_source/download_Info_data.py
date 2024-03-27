# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/20
# @Author  : gao
# @File    : download_Info_data.py
# @Project : AmazingQuant 
# ------------------------------

import pandas as pd
import tgw

from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.config.industry_class import sw_industry_one
from AmazingQuant.constant import LocalDataFolderName


class DownloadInfoData(object):
    def __init__(self, tgw_api_object):
        self.tgw_api_object = tgw_api_object
        self.code_list = []
        self.calendar_index = []

    def get_code_list(self, para_code_list='stock_list'):
        if para_code_list == 'stock_list':
            # self.code_list = self.tgw_api_object.get_code_list(add_market=True, all_code=True)
            self.code_list = self.tgw_api_object.get_code_list_hist()
        elif para_code_list == 'index_list':
            self.code_list = self.tgw_api_object.get_code_list(add_market=True, all_code=True, index=True)
        elif para_code_list == 'sw_index_list':
            self.code_list = sw_industry_one.keys()
        return self.code_list

    def get_calendar_index(self):
        self.calendar_index = self.tgw_api_object.get_calendar()

    def download_info_data(self, id, para_code_list='stock_list', para_date=False):
        num = 1
        error_code_list = []
        result = {}
        self.code_list = self.get_code_list(para_code_list)
        print(len(self.code_list))
        for code in self.code_list:
            print(id, code, num)
            num += 1
            code_isalpha = False
            for i in code[:-3]:
                if i.isalpha():
                    code_isalpha = True
                    break
            if code_isalpha:
                continue
            task_id = tgw.GetTaskID()
            tgw.SetThirdInfoParam(task_id, "function_id", id)
            if para_code_list == 'stock_list':
                tgw.SetThirdInfoParam(task_id, "market_code", code)
            elif para_code_list in ['index_list', 'sw_index_list']:
                tgw.SetThirdInfoParam(task_id, "index_code", code)

            if para_date:
                tgw.SetThirdInfoParam(task_id, "start_date", "19900101")
                tgw.SetThirdInfoParam(task_id, "end_date", "20991231")

            df, error = tgw.QueryThirdInfo(task_id)
            result[code] = df
            if error != 0:
                error_code_list.append(code)
                print('error', type(error), error, error_code_list)
        return pd.concat(result.values()), error_code_list

    def download_industry_class(self):
        """
        行业分类 A010010002
        """
        industry_class_df, error_code_list = self.download_info_data('A010010002')
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'industry_class', industry_class_df)
        return industry_class_df

    def download_index_member(self):
        """
        交易所指数成分股（含历史） A010200002
        """
        index_member_df, error_code_list = self.download_info_data('A010200002', para_code_list='index_list')
        folder_name = LocalDataFolderName.INDEX_MEMBER.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'index_member', index_member_df)
        return index_member_df

    def download_sw_index_member(self):
        """
        申万指数成分股（含历史） A010200003
        """
        index_member_df, error_code_list = self.download_info_data('A010200003', para_code_list='sw_index_list')
        folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'sw_industry_one', index_member_df)
        return index_member_df

    def download_stock_struction(self):
        """
        股本结构 A010010004
        """
        stock_struction_df, error_code_list = self.download_info_data('A010010004', para_date=True)
        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'stock_struction', stock_struction_df)
        return stock_struction_df

    def download_finance_data(self):
        """
        A股一般企业资产负债表  A010050001
        A股一般企业利润表     A010050002
        A股一般企业现金流表   A010050003
        """
        data_dict = {"A010050001": "balance", "A010050002": "income", "A010050003": "cash_flow"}
        result = {}
        for key, value in data_dict.items():
            result[value], error_code_list = self.download_info_data(key, para_date=True)
            folder_name = LocalDataFolderName.FINANCE.value
            path = LocalDataPath.path + folder_name + '/'
            save_data_to_hdf5(path, value, result[value])
        return result

    def download_longhubang(self):
        """
        交易异动营业部买卖信息 A010070002
        """
        longhubang_df, error_code_list = self.download_info_data('A010070002', para_date=True)

        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'longhubang', longhubang_df)
        return longhubang_df

    def download_10_shareholder(self):
        """
        A股十大股东名单 A010040001
        """
        shareholder_df, error_code_list = self.download_info_data('A010040001', para_date=True)
        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        save_data_to_hdf5(path, 'shareholder', shareholder_df[shareholder_df['HOLDER_TYPE'] == 10])
        save_data_to_hdf5(path, 'floatshareholder', shareholder_df[shareholder_df['HOLDER_TYPE'] == 20])
        return shareholder_df

    def download_hist_codelist(self, id='A010010008', interval=250):
        """
        历史代码列表(含期货、期权、指数) A010010007
        历史代码列表(含期货、期权、指数) A010010008
        """
        self.calendar_index = self.tgw_api_object.get_calendar()
        calendar_list = []
        error_code_list = []
        result = []
        num = 0
        for i in range(0, len(self.calendar_index), interval):
            start_date = str(self.calendar_index[i])
            try:
                end_date = str(self.calendar_index[i + interval - 1])
            except IndexError:
                end_date = str(self.calendar_index[-1])
            calendar_list.append([start_date, end_date])
        for date_list in calendar_list:
            print(id, date_list, num)
            num += 1
            task_id = tgw.GetTaskID()
            tgw.SetThirdInfoParam(task_id, "function_id", id)
            tgw.SetThirdInfoParam(task_id, "start_date", date_list[0])
            tgw.SetThirdInfoParam(task_id, "end_date", date_list[1])
            df, error = tgw.QueryThirdInfo(task_id)
            result.append(df)
            if error != 0:
                error_code_list.append(date_list)
                print('error', type(error), error, date_list)
        result_df = pd.concat(result)
        result_df.drop_duplicates(subset=['MARKET_CODE'], inplace=True)

        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        if id == 'A010010007':
            save_data_to_hdf5(path, 'hist_codelist1', result_df)
        elif id == 'A010010008':
            save_data_to_hdf5(path, 'hist_codelist2', result_df)

        return result_df, error_code_list


if __name__ == '__main__':
    tgw_login()
    tgw_api_object = TgwApiData()
    info_data_object = DownloadInfoData(tgw_api_object)
    # industry_class_df = info_data_object.download_industry_class()
    # index_member_df = info_data_object.download_index_member()
    # shareholder_df = info_data_object.download_10_shareholder()
    # sw_index_member_df = info_data_object.download_sw_index_member()
    # info_data_object.download_stock_struction()
    result = info_data_object.download_finance_data()
    # hist_codelist1 = info_data_object.download_hist_codelist(id='A010010007')
    # hist_codelist2 = info_data_object.download_hist_codelist(id='A010010008')


    # folder_name = LocalDataFolderName.INDUSTRY_CLASS.value
    # path = LocalDataPath.path + folder_name + '/'
    # a = get_local_data(path, folder_name + '.h5')
