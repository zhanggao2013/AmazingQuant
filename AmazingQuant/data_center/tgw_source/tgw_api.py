# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : tgw_api.py 
# @Project : AmazingQuant 
# ------------------------------
import tgw

from AmazingQuant.utils.data_transfer import date_to_datetime, datetime_to_int
from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login


class TgwApiData(object):
    def __init__(self, end_date):
        self.end_date = end_date
        self.calendar = []
        self.code_sh_list, self.code_sz_list = [], []
        self.stock_list = []
        self.code_list_hist = []

    def get_calendar(self, data_type=None):
        task_id = tgw.GetTaskID()
        tgw.SetThirdInfoParam(task_id, "function_id", "A010060001")
        tgw.SetThirdInfoParam(task_id, "start_date", "19900101")
        tgw.SetThirdInfoParam(task_id, "end_date", "20231231")
        tgw.SetThirdInfoParam(task_id, "market", 'SSE')

        trade_days_df, _ = tgw.QueryThirdInfo(task_id)
        trade_days_df['TRADE_DAYS'] = trade_days_df['TRADE_DAYS'].astype(int)
        self.calendar = list(trade_days_df['TRADE_DAYS'].sort_values(ascending=True))
        if data_type == 'datetime':
            self.calendar = [date_to_datetime(str(i)) for i in self.calendar]
        return self.calendar

    def get_code_list(self, add_market=False, all_code=False, index=False):
        for market in [tgw.MarketType.kSZSE, tgw.MarketType.kSSE]:
            item = tgw.SubCodeTableItem()
            item.market = market
            item.security_code = ""
            code_table_df, error = tgw.QuerySecuritiesInfo(item)
            # print('code_table_df', code_table_df['security_type'].unique())
            if index:
                code_table_df = code_table_df[code_table_df['security_type'].isin(['01000'])]
            else:
                code_table_df = code_table_df[code_table_df['security_type'].isin(['02001', '02003', '02004', '02999'])]
            code_list = list(code_table_df['security_code'])
            if market == tgw.MarketType.kSZSE:
                self.code_sz_list = code_list
                if add_market:
                    self.code_sz_list = [i + '.SZ' for i in self.code_sz_list]
            elif market == tgw.MarketType.kSSE:
                self.code_sh_list = code_list
                if add_market:
                    self.code_sh_list = [i + '.SH' for i in self.code_sh_list]

        if all_code:
            self.stock_list = self.code_sh_list + self.code_sz_list
            return self.stock_list
        else:
            return self.code_sh_list, self.code_sz_list

    def get_code_list_hist(self):
        task_id = tgw.GetTaskID()
        tgw.SetThirdInfoParam(task_id, "function_id", "A010010006")
        tgw.SetThirdInfoParam(task_id, "start_date", "19000101")
        tgw.SetThirdInfoParam(task_id, "end_date", "20991231")
        df, error = tgw.QueryThirdInfo(task_id)
        self.code_list_hist = list(df['MARKET_CODE'])
        return self.code_list_hist


if __name__ == '__main__':
    tgw_login()

    tgw_api_object = TgwApiData(20991231)
    calendar = tgw_api_object.get_calendar()
