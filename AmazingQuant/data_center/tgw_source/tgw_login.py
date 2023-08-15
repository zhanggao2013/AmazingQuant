# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : tgw_login.py
# @Project : AmazingQuant 
# ------------------------------

import tgw


from AmazingQuant.config.tgw_info import TgwConfig


class TgwLogSpi(tgw.ILogSpi):
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


def tgw_login(server_mode=False):
    log_spi = TgwLogSpi()
    tgw.SetLogSpi(log_spi)

    # 第二步，登录
    cfg = tgw.Cfg()
    cfg.server_vip = TgwConfig.host
    cfg.server_port = TgwConfig.port
    cfg.username = TgwConfig.username
    cfg.password = TgwConfig.password
    success = False
    # success = tgw.Login(cfg, tgw.ApiMode.kInternetMode, './')  # 互联网模式初始化，可指定证书文件地址
    if server_mode:
        cfg.coloca_cfg.channel_mode = tgw.ColocatChannelMode.kTCP | tgw.ColocatChannelMode.kQTCP \
                                      | tgw.ColocatChannelMode.kRTCP  # tcp订阅通道和查询通道初始化
        cfg.coloca_cfg.qtcp_channel_thread = 2
        cfg.coloca_cfg.qtcp_max_req_cnt = 1000
        cfg.coloca_cfg.enable_order_book = tgw.OrderBookType.kNone
        cfg.coloca_cfg.entry_size = 10
        cfg.coloca_cfg.order_queue_size = 10
        cfg.coloca_cfg.order_book_deliver_interval_microsecond = 10000
        success = tgw.Login(cfg, tgw.ApiMode.kColocationMode, './')  # 托管模式初始化，可指定证书文件地址
    if not success:
        print("login fail")
        exit(0)
