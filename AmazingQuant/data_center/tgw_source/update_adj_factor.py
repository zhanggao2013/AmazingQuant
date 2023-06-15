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

from AmazingQuant.config.tgw_info import TgwConfig

class MyLogSpi(tgw.ILogSpi):
    def __init__(self) -> None:
        super().__init__()
        pass

    def OnLog(self, level, log, len):
        if level > 1:
            # print("TGW log: level: {}     log:   {}".format(level, log.strip('\n').strip('\r')))
            pass

    def OnLogon(self, data):
        print("TGW Logon information:  : ")
        print("api_mode : ", data.api_mode)
        print("logon json : ", data.logon_json)


class SaveGetData(object):
    def __init__(self, path):
        self.path = path

    def save_data_to_hdf5(self, data_name, input_data, is_append=False):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        input_data.to_hdf(path + data_name + '.h5', key=data_name, mode='w', append=is_append)

    def get_local_data(self, data_name):
        return pd.read_hdf(self.path + data_name+'.h5')


class UpdateAdjFactor(object):
    def __init__(self):
        self.code_sh_list, self.code_sz_list = [], []

    def get_code_list(self):
        code_table_df, _ = tgw.QueryCodeTable(return_df_format=True)
        code_table_shsz_df = code_table_df[code_table_df['market_type'].isin([101, 102])]
        self.code_sh_list = list(
            code_table_shsz_df[code_table_shsz_df['security_type'].isin(['ASH', 'KSH'])]['security_code'])
        self.code_sz_list = list(
            code_table_shsz_df[code_table_shsz_df['security_type'].isin(['1', '2', '3'])]['security_code'])
        return self.code_sh_list, self.code_sz_list

    def get_adj_factor(self):

        tgw.QueryExFactorTable()



if __name__ == '__main__':
    # 第一步：设置日志spi，保证有日志输出
    log_spi = MyLogSpi()
    tgw.SetLogSpi(log_spi)

    # 第二步，登录
    cfg = tgw.Cfg()
    cfg.server_vip = TgwConfig.host
    cfg.server_port = TgwConfig.port
    cfg.username = TgwConfig.username
    cfg.password = TgwConfig.password

    success = tgw.Login(cfg, tgw.ApiMode.kInternetMode, './')  # 互联网模式初始化，可指定证书文件地址
    if not success:
        print("login fail")
        exit(0)

    adj_factor_object = UpdateAdjFactor()
    code_sh_list, code_sz_list = adj_factor_object.get_code_list()

    for market_type in [tgw.MarketType.kSSE, tgw.MarketType.kSZSE]:
        stock_kline.market_type = tgw.MarketType.kSSE
        code_list = self.code_sh_list
        if market_type == tgw.MarketType.kSZSE:
            stock_kline.market_type = tgw.MarketType.kSZSE
            code_list = self.code_sz_list

        for code in code_list: