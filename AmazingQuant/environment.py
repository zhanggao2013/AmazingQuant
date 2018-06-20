# -*- coding: utf-8 -*-

__author__ = "gao"

import pandas as pd

from AmazingQuant.data_object import *


class Environment(object):
    # key 都是每一根bar的timetag
    order_data_dict = {}  # timetag : [order_data,order_data]　　mission_engine risk 之后append
    deal_data_dict = {}  # timetag : [deal_data,deal_data]    broker_engine  deal 之后append
    position_data_dict = {}  # timetag : [position_data,position_data]  broker_engine deal 之后append
    account_data_dict = {}  # timetag : [account_data] ,account_data 只有一个，是当前bar最后一天的,main_engine market_close 之后append

    current_order_data = OrderData()
    current_deal_data = DealData()
    current_position_data = PositionData()
    current_account_data = AccountData()

    bar_order_data_list = []
    bar_deal_data_list = []
    bar_position_data_list = []
    bar_account_data_list = []

    daily_data = pd.DataFrame()
    one_min_data = pd.DataFrame()

    @classmethod
    def refresh(cls):
        cls.bar_order_data_list = []
        cls.bar_deal_data_list = []
