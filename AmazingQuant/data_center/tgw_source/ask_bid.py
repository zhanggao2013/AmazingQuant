# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/26
# @Author  : gao
# @File    : ask_bid.py
# @Project : AmazingQuant
# ------------------------------
import os
import time, datetime
import threading
import queue

import numpy as np
import pandas as pd
import tgw

from AmazingQuant.data_center.tgw_source.tgw_api import TgwApiData
from AmazingQuant.data_center.tgw_source.tgw_login import tgw_login

security_code_list = []
market_type_list = []

zhangfu_dict = {}
price_spread_dict = {}
volume_spread_dict = {}


# 实现推送回调
class DataHandler(tgw.IPushSpi):
    def __init__(self) -> None:
        super().__init__()
        self.queue = queue.Queue()
        for i in range(4):
            self.thread = threading.Thread(target=self.process_data)
            self.thread.start()

        self.thread_queue = threading.Thread(target=self.process_queue)
        self.thread_queue.start()

    def process_queue(self):
        while True:
            if self.queue.empty():
                continue
            print('qsize:', datetime.datetime.now(), self.queue.qsize())

    def process_data(self):
        while True:
            if not self.queue.empty():
                data = self.queue.get()

                data_queue = data.copy()
                global security_code_list
                global market_type_list
                if data_queue[0]['security_code'] not in security_code_list:
                    security_code_list.append(data_queue[0]['security_code'])
                    # print('security_code_list', len(security_code_list), data_queue[0]['security_code'])

                if data_queue[0]['market_type'] not in market_type_list:
                    market_type_list.append(data_queue[0]['market_type'])
                #     print('market_type_list', len(market_type_list))

                global zhangfu_dict
                if data_queue[0]['pre_close_price'] > 0:
                    zhangfu_dict[data_queue[0]['security_code']] = (data_queue[0]['last_price'] / data_queue[0][
                        'pre_close_price'] - 1) * 100
                else:
                    zhangfu_dict[data_queue[0]['security_code']] = np.nan
                global price_spread_dict
                price_spread_dict[data_queue[0]['security_code']] = (data_queue[0]['offer_price1'] - data_queue[0][
                    'bid_price1']) / 1000000

                global volume_spread_dict
                bid_volume_total = data_queue[0]['bid_volume1'] + data_queue[0]['bid_volume2'] + data_queue[0][
                    'bid_volume3'] + \
                                   data_queue[0]['bid_volume4'] + data_queue[0]['bid_volume5']
                offer_volume_total = data_queue[0]['offer_volume1'] + data_queue[0]['offer_volume2'] + data_queue[0][
                    'offer_volume3'] + \
                                     data_queue[0]['offer_volume4'] + data_queue[0]['offer_volume5']
                if offer_volume_total > 0:
                    volume_spread_dict[data_queue[0]['security_code']] = (bid_volume_total - offer_volume_total) / \
                                                                         offer_volume_total
                else:
                    volume_spread_dict[data_queue[0]['security_code']] = np.nan
                time.sleep(0.01)

    def OnMDSnapshot(self, data, err):
        if not data is None:
            self.queue.put(data)
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
    tgw_api_object = TgwApiData(20991231)
    code_sh_list, code_sz_list = tgw_api_object.get_code_list()
    print(len(code_sh_list), len(code_sz_list))
    sub_item_list = []
    data_hander = DataHandler()
    data_hander.SetDfFormat(False)
    # for code in code_sh_list:
    #     sub_item = tgw.SubscribeItem()
    #     sub_item.security_code = code
    #     sub_item.flag = tgw.SubscribeDataType.kSnapshot
    #     sub_item.category_type = tgw.VarietyCategory.kNone
    #     sub_item.market = tgw.MarketType.kSSE
    #     sub_item_list.append(sub_item)
    # for code in code_sz_list:
    #     sub_item = tgw.SubscribeItem()
    #     sub_item.security_code = code
    #     sub_item.flag = tgw.SubscribeDataType.kSnapshot
    #     sub_item.category_type = tgw.VarietyCategory.kNone
    #     sub_item.market = tgw.MarketType.kSZSE
    #     sub_item_list.append(sub_item)
    # success = tgw.Subscribe(sub_item_list, data_hander)

    sub_item = tgw.SubscribeItem()
    sub_item.security_code = ''
    sub_item.flag = tgw.SubscribeDataType.kSnapshot
    sub_item.category_type = tgw.VarietyCategory.kStock
    sub_item.market = tgw.MarketType.kSSE
    success_sh = tgw.Subscribe(sub_item, data_hander)
    print('success_sz', success_sh)
    if success_sh != tgw.ErrorCode.kSuccess:
        print(tgw.GetErrorMsg(success_sh))

    sub_item = tgw.SubscribeItem()
    sub_item.security_code = ''
    sub_item.flag = tgw.SubscribeDataType.kSnapshot
    sub_item.category_type = tgw.VarietyCategory.kStock
    sub_item.market = tgw.MarketType.kSZSE
    success_sz = tgw.Subscribe(sub_item, data_hander)

    print('success_sz', success_sz)
    if success_sz != tgw.ErrorCode.kSuccess:
        print(tgw.GetErrorMsg(success_sz))
    while True:
        try:
            if g_is_running != True:
                break
        except Exception as e:
            print(str(e))
        # time.sleep(1)
        # code = '688597'
        # if code in zhangfu_dict:
        #     print('zhangfu_dict', zhangfu_dict[code])
