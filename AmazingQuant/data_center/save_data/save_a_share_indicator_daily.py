# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : save_a_share_indicator_daily.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

import pandas as pd
from mongoengine.context_managers import switch_collection

from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.data_center.database_field.field_a_share_indicator_daily import AShareIndicatorDaily
from AmazingQuant.constant import DatabaseName


def save_a_share_indicator_daily(indicator_name, input_data):
    database = DatabaseName.A_SHARE_INDICATOR_DAILY.value
    with MongoConnect(database):
        with switch_collection(AShareIndicatorDaily, indicator_name) as indicator:
            doc_list = []
            # for index, row in input_data.iterrows():
            #     row_dict = dict(row)
            #     doc = AShareIndicatorDaily(time_tag=index, security_code_list=row_dict.keys(), data=row_dict.values())
            #     doc_list.append(doc)
            doc = AShareIndicatorDaily(time_tag=index, security_code_list=input_data.columns(), data=row_dict.values())
            indicator.objects.insert(doc_list)


if __name__ == '__main__':
    with Timer(True):
        pass
