# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/1/10
# @Author  : gao
# @File    : update_adj_factor.py
# @Project : AmazingQuant
# ------------------------------
import pandas as pd
import numpy as np

from AmazingQuant.utils.mongo_connection_me import MongoConnect
from apps.server.database_server.database_field.field_a_share_ex_right_dividend import AShareExRightDividend
from AmazingQuant.data_center.api_data.get_kline import GetKlineData
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.constant import DatabaseName, LocalDataFolderName, AdjustmentFactor
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_calender import GetCalendar


class SaveAShareAdjFactor(object):
    def __init__(self):
        self.data = pd.DataFrame()
        self.database = DatabaseName.STOCK_BASE_DATA.value

    def save_a_share_adj_factor_right(self):
        """
        取当日收盘价，作为转、送的股价，
        再计算复权因子更新到AShareExRightDividend, 复权因子adj_factor
        比例 = 送股比例 + 转增比例 + 缩减比例
        单次复权因子 = 股权登记日收盘价 * (1 + 比例 + 配股比例 + 增发比例) /
        (股权登记日收盘价 - 派息比例 + 股权登记日收盘价 * 比例 + 配股价格 * 配股比例 + 增发价格 * 增发比例)
        :return:
        """
        kline_object = GetKlineData()
        all_market_data = kline_object.cache_all_stock_data()
        with MongoConnect(self.database):
            self.data = pd.DataFrame(AShareExRightDividend.objects.as_pymongo())
            self.data['close'] = self.data.apply(
                lambda x: self.get_adj_day_close(x['security_code'], x['ex_date'], all_market_data), axis=1)
            self.data = self.data.fillna(0)
            ratio = self.data['bonus_share_ratio'] + self.data['conversed_ratio'] + self.data['consolidate_split_ratio']
            self.data['adj_factor'] = self.data['close'] * (
                        1 + ratio + self.data['rightsissue_ratio'] + self.data['seo_ratio']) / (
                        self.data['close'] - self.data['cash_dividend_ratio'] + self.data['close'] * ratio +
                        self.data['rightsissue_price'] * self.data['rightsissue_ratio'] +
                        self.data['seo_price'] * self.data['seo_ratio'])

            folder_name = LocalDataFolderName.ADJ_FACTOR.value
            path = LocalDataPath.path + folder_name + '/'
            self.data = self.data.reindex(columns=['security_code', 'ex_date', 'adj_factor'])
            self.data.set_index(["ex_date"], inplace=True)
            self.data.sort_index(inplace=True)
            calendar_obj = GetCalendar()
            calendar = calendar_obj.get_calendar('SZ')
            backward_factor = pd.DataFrame(index=calendar)
            adj_factor = pd.DataFrame(index=calendar)
            data_dict = dict(list(self.data.groupby(self.data['security_code'])))
            for security_code, adj_data in data_dict.items():
                backward_factor[security_code] = self.cal_backward_factor(adj_data['adj_factor'])
                adj_factor[security_code] = adj_data['adj_factor']
            backward_factor.replace([np.inf, 0], np.nan, inplace=True)
            backward_factor.fillna(method='ffill', inplace=True)
            backward_factor.fillna(1, inplace=True)
            save_data_to_hdf5(path, AdjustmentFactor.BACKWARD_ADJ_FACTOR.value, backward_factor)
            save_data_to_hdf5(path, AdjustmentFactor.FROWARD_ADJ_FACTOR.value, backward_factor.div(backward_factor.iloc[-1]))

    def cal_backward_factor(self, x):
        result = pd.Series(index=x.index)
        a = 1
        for i in range(len(x)):
            result[i] = x[i]*a
            a = result[i]
        return result

    def get_adj_day_close(self, security_code, date, all_market_data):
        security_code_market_data = 0
        try:
            security_code_market_data = all_market_data['close'].loc[date, security_code]
        except KeyError:
            print(security_code, date, security_code_market_data)
        return security_code_market_data


if __name__ == '__main__':
    save_a_share_adj_factor_obj = SaveAShareAdjFactor()
    save_a_share_adj_factor_obj.save_a_share_adj_factor_right()
