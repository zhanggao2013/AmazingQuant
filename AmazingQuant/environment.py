# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : environment.py.py
# @Project : AmazingQuant
# ------------------------------
import copy

import pandas as pd

from AmazingQuant.data_object import *


class Environment(object):

    # 日志工具，必须先初始化
    logger = None
    # key 都是每一根bar的timetag
    order_data_dict = {}  # timetag : [order_data,order_data]　　mission_engine risk 之后append
    deal_data_dict = {}  # timetag : [deal_data,deal_data]    broker_engine  deal 之后append
    position_data_dict = {}  # timetag : [position_data,position_data]  broker_engine deal 之后append
    account_data_dict = {}  # timetag : [account_data] ,account_data 只有一个，是当前bar最后一天的,main_engine market_close 之后append

    current_order_data = copy.deepcopy(order_data)
    current_deal_data = copy.deepcopy(deal_data)
    current_position_data = copy.deepcopy(position_data)
    current_account_data = copy.deepcopy(account_data)

    bar_order_data_list = []
    bar_deal_data_list = []
    bar_position_data_list = []
    bar_account_data_list = []

    daily_data = pd.DataFrame()
    one_min_data = pd.DataFrame()

    index_daily_data = pd.DataFrame()

    benchmark_index = []

    # 风控部分
    black_namelist = []
    is_pass_risk = True
    is_send_order = False

    # 回测滑点,key是股票，或者具体的期货代码
    slippage_dict = {}
    # 回测手续费,key是股票，或者具体的期货代码
    commission_dict = {}

    # 每根bar结束，清空的当前bar的order 和　deal的list
    @classmethod
    def refresh_list(cls, event):
        cls.bar_order_data_list = []
        cls.bar_deal_data_list = []

    # 回测交易记录
    backtesting_record_order = pd.DataFrame()
    backtesting_record_deal = pd.DataFrame()
    backtesting_record_position = pd.DataFrame()
    backtesting_record_account = pd.DataFrame()

    # 每次下单交易完成，经过回测broker之后清空order和deal的数据，重置是否通过风控
    @classmethod
    def refresh_current_data(cls, event):
        cls.current_order_data = copy.deepcopy(order_data)
        cls.current_deal_data = copy.deepcopy(deal_data)
        cls.current_position_data = copy.deepcopy(position_data)
        cls.is_pass_risk = True
        cls.is_send_order = False

    @classmethod
    def refresh_backtesting_record(cls, event):
        Environment.backtesting_record_order = pd.DataFrame()
        Environment.backtesting_record_deal = pd.DataFrame()
        Environment.backtesting_record_position = pd.DataFrame()
        Environment.backtesting_record_account = pd.DataFrame()
        Environment.bar_order_data_list = []
        Environment.bar_deal_data_list = []
        Environment.bar_position_data_list = []
        Environment.bar_account_data_list = []

