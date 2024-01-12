# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : download_adj_factor.py
# @Project : AmazingQuant 
# ------------------------------
import datetime

import numpy as np
import pandas as pd
import tgw

from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import LocalDataFolderName, AdjustmentFactor
from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login
from AmazingQuant.utils.save_data import save_data_to_hdf5
from AmazingQuant.utils.data_transfer import date_to_datetime


class UpdateAdjFactor(object):
    def __init__(self):
        pass

    def get_backward_factor(self, code_sh_list, code_sz_list, calendar_index):
        adj_factor_date_min = min(calendar_index)
        market = 'SH'
        num = 1
        backward_factor_list = []
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            code_list = code_sh_list
            if market_type == tgw.MarketType.kSZSE:
                code_list = code_sz_list
                market = 'SZ'
            for code in code_list:
                print(code, 'adj_factor', num)
                num += 1
                adj_factor, error = tgw.QueryExFactorTable(code)
                if adj_factor is None:
                    adj_factor = pd.DataFrame({}, columns=['cum_factor', 'ex_date'])
                adj_factor.set_index(["ex_date"], inplace=True)
                adj_factor.sort_index(inplace=True)

                if not adj_factor.empty:
                    adj_factor_code = pd.DataFrame(adj_factor['cum_factor'])
                    adj_factor_code.columns = [code + '.' + market]
                    backward_factor_list.append(adj_factor_code)
                else:
                    backward_factor_list.append(pd.DataFrame(np.nan,
                                                             columns=[code + '.' + market],
                                                             index=calendar_index))
        backward_factor = pd.concat(backward_factor_list, axis=1)
        index_add = list(set(calendar_index) - set(backward_factor.index))
        backward_factor = pd.concat([backward_factor,
                                     pd.DataFrame(np.nan, columns=backward_factor.columns, index=index_add)])
        backward_factor.sort_index(inplace=True)
        backward_factor.replace([np.inf, 0], np.nan, inplace=True)
        backward_factor.fillna(method='ffill', inplace=True)
        backward_factor.fillna(1, inplace=True)
        backward_factor = backward_factor.loc[calendar_index, :]

        backward_factor.index = pd.Series([date_to_datetime(str(i)) for i in backward_factor.index])
        return backward_factor

    def get_backward_factor_ratio(self, close_df, code_sh_list, code_sz_list, calendar_index):
        """
        取当日收盘价，作为转、送的股价，
        再计算复权因子更新到AShareExRightDividend, 复权因子adj_factor
        比例 = 送股比例 + 转增比例 + 缩减比例
        单次复权因子 = 股权登记日收盘价 * (1 + 比例 + 配股比例 + 增发比例) /
        (股权登记日收盘价 - 派息比例 + 股权登记日收盘价 * 比例 + 配股价格 * 配股比例 + 增发价格 * 增发比例)
        :return:
        """
        ex_right_dividend_df = None
        market = 'SH'
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            code_list = code_sh_list
            if market_type == tgw.MarketType.kSZSE:
                code_list = code_sz_list
                market = 'SZ'
            for code in code_list:
                task_id = tgw.GetTaskID()
                tgw.SetThirdInfoParam(task_id, "function_id", "A010030003")
                tgw.SetThirdInfoParam(task_id, "start_date", "20130101")
                tgw.SetThirdInfoParam(task_id, "end_date", "20991231")
                tgw.SetThirdInfoParam(task_id, "market_code", code + '.' + market)
                df, _ = tgw.QueryThirdInfo(task_id)
                if ex_right_dividend_df is None:
                    ex_right_dividend_df = df
                else:
                    ex_right_dividend_df = ex_right_dividend_df.append(df)

        ex_right_dividend_df['close'] = ex_right_dividend_df.apply(
            lambda x: self.get_adj_day_close(x['MARKET_CODE'], int(x['EX_RD_DATE']), close_df), axis=1)
        ex_right_dividend_df = ex_right_dividend_df.fillna(0)
        ratio = ex_right_dividend_df['BONUS_SHARE_RATIO'] + ex_right_dividend_df['CONVER_INCR_RATIO'] + \
                ex_right_dividend_df['REDUCED_RATIO']

        ex_right_dividend_df['adj_factor'] = ex_right_dividend_df['close'] * (
                1 + ratio + ex_right_dividend_df['RIGHT_ISSUE_RATIO'] + ex_right_dividend_df['SEO_RATIO']) / (
                                                     ex_right_dividend_df['close'] - ex_right_dividend_df[
                                                 'DIV_PAYOUT_RATIO'] + ex_right_dividend_df['close']
                                                     * ratio + ex_right_dividend_df['RIGHT_ISSUE_PRICE'] *
                                                     ex_right_dividend_df['RIGHT_ISSUE_RATIO'] +
                                                     ex_right_dividend_df['SEO_PRICE'] * ex_right_dividend_df[
                                                         'SEO_RATIO'])
        ex_right_dividend_df = ex_right_dividend_df.reindex(
            columns=['MARKET_CODE', 'EX_RD_DATE', 'adj_factor', 'close'])
        ex_right_dividend_df["EX_RD_DATE"] = ex_right_dividend_df["EX_RD_DATE"].astype(int)
        ex_right_dividend_df.set_index(["EX_RD_DATE"], inplace=True)
        ex_right_dividend_df.sort_index(inplace=True)

        ex_right_dividend_df.fillna(method='ffill', inplace=True)

        backward_factor_ratio = pd.DataFrame(index=calendar_index)
        data_dict = dict(list(ex_right_dividend_df.groupby(ex_right_dividend_df['MARKET_CODE'])))
        for security_code, adj_data in data_dict.items():
            backward_factor_ratio[security_code] = adj_data['adj_factor'].cumprod(axis=0)

        backward_factor_ratio.replace([np.inf, 0], np.nan, inplace=True)
        backward_factor_ratio.fillna(method='ffill', inplace=True)
        backward_factor_ratio.fillna(1, inplace=True)
        backward_factor_ratio.sort_index(inplace=True)

        return backward_factor_ratio, ex_right_dividend_df, data_dict

    def get_adj_day_close(self, security_code, date, close_df):
        security_code_market_data = 0
        try:
            security_code_market_data = close_df.loc[date, security_code] / 1000000
        except KeyError:
            print(security_code, date, security_code_market_data)
        return security_code_market_data

    def cal_forward_factor(self, backward_factor):
        forward_factor = backward_factor.div(backward_factor.iloc[-1])
        return forward_factor.loc[datetime.datetime(2013, 1, 1):]


if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData()
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    calendar_index = tgw_api_object.get_calendar()

    adj_factor_object = UpdateAdjFactor()
    backward_factor = adj_factor_object.get_backward_factor(code_sh_list, code_sz_list, calendar_index)

    folder_name = LocalDataFolderName.ADJ_FACTOR.value
    path = LocalDataPath.path + folder_name + '/'
    save_data_to_hdf5(path, AdjustmentFactor.BACKWARD_ADJ_FACTOR.value, backward_factor)

    forward_factor = adj_factor_object.cal_forward_factor(backward_factor)
    save_data_to_hdf5(path, AdjustmentFactor.FROWARD_ADJ_FACTOR.value, forward_factor)

    # # path = LocalDataPath.path + LocalDataFolderName.MARKET_DATA.value + '//' + LocalDataFolderName.KLINE_DAILY.value + \
    # #        '//' + LocalDataFolderName.A_SHARE.value + '//'
    # # close_df = get_local_data(path, 'close_price.h5')
    # # backward_factor_ratio = adj_factor_object.get_backward_factor_ratio(close_df, code_sh_list,  code_sz_list, calendar_index)
