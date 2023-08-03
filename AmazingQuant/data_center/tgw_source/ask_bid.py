# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/26
# @Author  : gao
# @File    : ask_bid.py 
# @Project : AmazingQuant 
# ------------------------------
import os
import time, datetime

import pandas as pd
import tgw

from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login


# 实现推送回调
class DataHandler(tgw.IPushSpi):
    def __init__(self) -> None:
        super().__init__()

    def OnMDSnapshot(self, data, err):
        if not data is None:
            if data[0]['security_code'] == '000002':
                print(data[0]['orig_time'], data[0]['last_price']/1000000)
            pass
        else:
            print(err)

    def OnMDIndexSnapshot(self, data, err):
        if not data is None:
            pass
        else:
            print(err)


if __name__ == "__main__":
    tgw_login()
    g_is_running = True

    data_hander = DataHandler()
    data_hander.SetDfFormat(False)
    sub_item = tgw.SubscribeItem()
    sub_item.security_code = "000002"
    sub_item.SubscribeDataType = tgw.SubscribeDataType.kSnapshot
    sub_item.VarietyCategory = tgw.VarietyCategory.kStock
    sub_item.market = tgw.MarketType.kNone
    success = tgw.Subscribe(sub_item, data_hander)
    print('success', success)
    if success != tgw.ErrorCode.kSuccess:
        print(tgw.GetErrorMsg(success))
    while True:
        try:
            if g_is_running != True:
                break
        except Exception as e:
            print(str(e))
        time.sleep(1)
