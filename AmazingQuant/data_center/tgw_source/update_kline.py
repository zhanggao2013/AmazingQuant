# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : update_kline.py
# @Project : AmazingQuant
# ------------------------------
import os
import time

import pandas as pd
import tgw


class MyLogSpi(tgw.ILogSpi):
    def __init__(self) -> None:
        super().__init__()
        pass

    def OnLog(self, level, log, len):
        if level > 1:
            print("TGW log: level: {}     log:   {}".format(level, log.strip('\n').strip('\r')))
            pass

    def OnLogon(self, data):
        print("TGW Logon information:  : ")
        print("api_mode : ", data.api_mode)
        print("logon json : ", data.logon_json)


class UpdateKlineData(object):
    def __init__(self, end_date):
        self.field = ['kline_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume_trade',
                      'value_trade']
        self.end_date = end_date
        self.calendar = []
        self.code_sh_list, self.code_sz_list = [], []

    def get_calendar(self):
        index_kline = tgw.ReqKline()
        index_kline.cq_flag = 0
        index_kline.auto_complete = 1
        index_kline.cyc_type = tgw.MDDatatype.kDayKline
        index_kline.begin_date = 19900101
        index_kline.end_date = self.end_date
        index_kline.begin_time = 930
        index_kline.end_time = 1700

        index_kline.security_code = '000001'
        index_kline.market_type = tgw.MarketType.kSSE

        index_kline_df, _ = tgw.QueryKline(index_kline)

        self.calendar = list(index_kline_df['kline_time'])
        return self.calendar

    def get_code_list(self):
        code_table_df, _ = tgw.QueryCodeTable(return_df_format=True)
        code_table_shsz_df = code_table_df[code_table_df['market_type'].isin([101, 102])]
        self.code_sh_list = list(
            code_table_shsz_df[code_table_shsz_df['security_type'].isin(['ASH', 'KSH'])]['security_code'])
        self.code_sz_list = list(
            code_table_shsz_df[code_table_shsz_df['security_type'].isin(['1', '2', '3'])]['security_code'])
        return self.code_sh_list, self.code_sz_list

    def get_kline_data(self):
        stock_kline = tgw.ReqKline()
        stock_kline.cq_flag = 0
        stock_kline.auto_complete = 1
        stock_kline.cyc_type = tgw.MDDatatype.kDayKline
        stock_kline.begin_date = 19900101
        stock_kline.end_date = 20991231
        stock_kline.begin_time = 930
        stock_kline.end_time = 1700

        # 获取深圳/上海股票的行情
        stock_data_dict = {}
        for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
            stock_kline.market_type = tgw.MarketType.kSSE
            code_list = self.code_sh_list
            if market_type == tgw.MarketType.kSZSE:
                stock_kline.market_type = tgw.MarketType.kSZSE
                code_list = self.code_sz_list

            for code in code_list[:5]:
                stock_kline.security_code = code
                stock_data_df, _ = tgw.QueryKline(stock_kline)
                stock_data_df = stock_data_df[self.field]
                stock_data_df.set_index(["kline_time"], inplace=True)
                stock_data_df = stock_data_df.reindex(self.calendar).fillna(method='ffill')
                stock_data_dict[code] = stock_data_df

        return stock_data_dict


class SaveGetData(object):
    def __init__(self, path):
        self.path = path

    def save_data_to_hdf5(self, data_name, input_data, is_append=False):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        input_data.to_hdf(path + data_name + '.h5', key=data_name, mode='w', append=is_append)

    def get_local_data(self, data_name):
        return pd.read_hdf(self.path + data_name+'.h5')


if __name__ == '__main__':
    # 第一步：设置日志spi，保证有日志输出
    log_spi = MyLogSpi()
    tgw.SetLogSpi(log_spi)

    # 第二步，登录
    cfg = tgw.Cfg()
    cfg.server_vip = "101.230.159.234"
    cfg.server_port = 8600
    cfg.username = "zdg"  # 账号
    cfg.password = "zdg@2022"  # 密码

    success = tgw.Login(cfg, tgw.ApiMode.kInternetMode, './')  # 互联网模式初始化，可指定证书文件地址
    if not success:
        print("login fail")
        exit(0)

    kline_object = UpdateKlineData(20991231)
    code_sh_list, code_sz_list = kline_object.get_code_list()
    calendar_index = kline_object.get_calendar()
    stock_data_dict = kline_object.get_kline_data()

    local_data_path = 'D://AmazingQuant//local_data//'
    folder_name = 'market_data'
    sub_folder_name = 'kline_daily'
    sub_sub_folder_name = 'a_share'
    path = local_data_path + folder_name + '//' + sub_folder_name + '//' + sub_sub_folder_name + '//'
    save_get_data = SaveGetData(path)

    field_data_dict = {}
    for i in kline_object.field:
        if i != 'kline_time':
            field_data_pd = pd.DataFrame({key: value[i] for key, value in stock_data_dict.items()})
            field_data_dict[i] = field_data_pd
            save_get_data.save_data_to_hdf5(i, field_data_pd)

    close = save_get_data.get_local_data('close_price')

