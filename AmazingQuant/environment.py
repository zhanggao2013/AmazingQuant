# -*- coding: utf-8 -*-

__author__ = "gao"

import pandas as pd

from AmazingQuant.data_object import *


class Environment(object):
    # key 都是每一根bar的timetag
    order_data_dict = {}    # timetag : [order_data,order_data]　　mission_engine risk 之后append
    deal_data_dict = {}    # timetag : [deal_data,deal_data]    broker_engine  deal 之后append
    position_data_dict = {}  # timetag : [position_data,position_data]  broker_engine deal 之后append
    account_data_dict = {}   # timetag : [account_data] ,account_data 只有一个，是当前bar最后一天的,main_engine market_close 之后append

    current_order_data = OrderData()
    current_deal_data = DealData()
    current_position_data = PositionData()
    current_account_data = AccountData()

    @classmethod
    def refresh(cls):
        cls.current_order_data = OrderData()
        cls.current_deal_data = DealData()
        cls.current_position_data = PositionData()
        cls.current_account_data = AccountData()
