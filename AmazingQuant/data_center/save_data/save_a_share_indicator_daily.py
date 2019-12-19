# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : save_a_share_indicator_daily.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime
import pickle

import pandas as pd
from mongoengine.context_managers import switch_collection

from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.utils.code_transfer import code_market_to_market_code
from AmazingQuant.data_center.database_field.field_a_share_indicator_daily import AShareIndicatorDaily
from AmazingQuant.constant import DatabaseName


def save_a_share_indicator_daily(indicator_name, input_data):
    database = DatabaseName.A_SHARE_INDICATOR_DAILY.value
    with MongoConnect(database):
        with switch_collection(AShareIndicatorDaily, indicator_name) as indicator:
            doc_list = []
            input_data = input_data.rename(columns={i: code_market_to_market_code(i) for i in input_data})
            print(input_data.columns)
            # for index, row in input_data.iterrows():
            #     row_dict = dict(row)
            #     doc = AShareIndicatorDaily(time_tag=index, data=row_dict)
            #     doc_list.append(doc)
            # indicator.objects.insert(doc_list)
            doc = indicator(data=pickle.dumps(input_data))
            doc.save()


def get_a_share_indicator_daily(indicator_name):
    database = DatabaseName.A_SHARE_INDICATOR_DAILY.value
    with MongoConnect(database):
        with switch_collection(AShareIndicatorDaily, indicator_name) as indicator:
            obj_list = indicator.objects()
            for i in obj_list:
                result = pickle.loads(i.data)
    return result


if __name__ == '__main__':
    with Timer(True):
        a = get_a_share_indicator_daily('close')
