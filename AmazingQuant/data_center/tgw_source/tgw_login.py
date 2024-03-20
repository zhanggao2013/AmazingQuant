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
    cfg.username = TgwConfig.username
    cfg.password = TgwConfig.password
    success = False
    if server_mode:
        cfg.server_vip = TgwConfig.host2
        cfg.server_port = TgwConfig.port2
        cfg.coloca_cfg.channel_mode = tgw.ColocatChannelMode.kTCP | tgw.ColocatChannelMode.kQTCP \
                                      | tgw.ColocatChannelMode.kRTCP  # tcp订阅通道和查询通道初始化
        cfg.coloca_cfg.qtcp_channel_thread = 10
        cfg.coloca_cfg.qtcp_max_req_cnt = 1000
        cfg.coloca_cfg.enable_order_book = tgw.OrderBookType.kNone
        cfg.coloca_cfg.entry_size = 10
        cfg.coloca_cfg.order_queue_size = 10
        cfg.coloca_cfg.order_book_deliver_interval_microsecond = 10000
        success = tgw.Login(cfg, tgw.ApiMode.kColocationMode, './')  # 托管模式初始化，可指定证书文件地址
    else:
        cfg.server_vip = TgwConfig.host1
        cfg.server_port = TgwConfig.port1
        success = tgw.Login(cfg, tgw.ApiMode.kInternetMode, './')  # 互联网模式初始化，可指定证书文件地址

    if not success:
        print("login fail")
        exit(0)


if __name__ == '__main__':

    tgw_login(server_mode=True)


    # 第一步： 定义回放数据回调函数
    # K 线回放处理函数
    def OnResponseKline(task_id, result, err):
        if not result is None:
            print("Kline:", result)

        else:
            print(err)


    # 快照数据回放处理函数
    def OnResponseSnapshot(task_id, result, err):
        if not result is None:
            print("Snapshot:",result)

        else:
            print(err)


    # 逐笔成交数据回放处理函数
    def OnResponseTickExec(task_id, result, err):
        if not result is None:
            print("TickExecution:", result)

        else:
            print(err)


    root = './'
    return_DF = True
    # 回放快照
    # replay_cfg = tgw.ReplayCfg()
    # replay_cfg.begin_date = 20230518
    # replay_cfg.end_date = 20230519
    # replay_cfg.begin_time = 90000000
    # replay_cfg.end_time = 103100000
    # replay_cfg.task_id = tgw.GetTaskID()
    # replay_cfg.req_codes = [(tgw.MarketType.kSSE, "600000")]  # 支持多代码回放
    # replay_cfg.md_data_type = tgw.MDDatatype.kSnapshot
    # # 第二参数设置事先已经定义好的相应回调处理函数
    # ret = tgw.ReplayRequest(replay_cfg, OnResponseSnapshot, return_df_format=return_DF)
    # # 查询参数 return_df_format 可设置数据返回格式： True： DataFrame格式False： json格式
    # if ret == tgw.ErrorCode.kSuccess:
    #     pass
    # else:
    #     print(tgw.GetErrorMsg(ret))
    # # 回放逐笔成交
    # replay_cfg = tgw.ReplayCfg()
    # replay_cfg.begin_date = 20230519
    # replay_cfg.end_date = 20230519
    # replay_cfg.begin_time = 90000000
    # replay_cfg.end_time = 103100000
    # replay_cfg.task_id = tgw.GetTaskID()
    # replay_cfg.req_codes = [(tgw.MarketType.kSSE, "600000")]  # 支持多代码回放
    # replay_cfg.md_data_type = tgw.MDDatatype.kTickExecution
    # # 第二参数设置事先已经定义好的相应回调处理函数
    # ret = tgw.ReplayRequest(replay_cfg, OnResponseTickExec, return_df_format=return_DF)
    #
    # if ret == tgw.ErrorCode.kSuccess:
    #     pass
    # else:
    #     print(tgw.GetErrorMsg(ret))
    # 回放 k 线
    # replay_cfg = tgw.ReplayCfg()
    # replay_cfg.cq_flag = 0
    # replay_cfg.cyc_type = tgw.MDDatatype.k1KLine
    # replay_cfg.auto_complete = 1
    # replay_cfg.begin_date = 20230519
    # replay_cfg.end_date = 20230519
    # replay_cfg.begin_time = 930
    # replay_cfg.end_time = 1532
    #                                                                                                                                                                                                                                     replay_cfg.req_codes = [(tgw.MarketType.kSZSE, "000001"),
    #                         (tgw.MarketType.kSSE, "600000")]  # 支持多代码回放中国银河证券星耀数智服务平台金融数据功能开发手册（Python 版）
    #
    # # 第二参数设置事先已经定义好的相应回调处理函数
    # ret = tgw.ReplayKline(replay_cfg, OnResponseKline, return_df_format=return_DF)
    # if ret == tgw.ErrorCode.kSuccess:
    #
    #
    #     pass
    # else:
    #     print(tgw.GetErrorMsg(ret))
