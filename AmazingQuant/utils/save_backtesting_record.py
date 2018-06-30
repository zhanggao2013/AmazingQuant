# -*- coding: utf-8 -*-

__author__ = "gao"

import sys
import os
import time
import copy

import pandas as pd

from AmazingQuant.environment import Environment
from AmazingQuant.constant import RecordDataType


class EmptyClass(object):
    pass


def save_backtesting_record_to_csv(data_type=RecordDataType.ACCOUNT_DATA.value):
    if data_type == RecordDataType.ORDER_DATA.value:
        data_obj = Environment.current_order_data
        data_dict = Environment.order_data_dict

    elif data_type == RecordDataType.DEAL_DATA.value:
        data_obj = Environment.current_deal_data
        data_dict = Environment.deal_data_dict

    elif data_type == RecordDataType.POSITION_DATA.value:
        data_obj = Environment.current_position_data
        data_dict = Environment.position_data_dict

    elif data_type == RecordDataType.ACCOUNT_DATA.value:
        data_obj = Environment.current_account_data
        data_dict = Environment.account_data_dict

    data_property = [i for i in dir(data_obj) if i not in dir(copy.deepcopy(EmptyClass()))]
    print(data_property, dir(copy.deepcopy(EmptyClass)))
    values = []
    for timetag in Environment.benchmark_index:
        timetag_data_list = []
        for current_data in data_dict[timetag]:
            timetag_data_list.append([current_data.__dict__[property_data] for property_data in data_property])
        print(timetag_data_list)
        timetag_data_df = pd.DataFrame(timetag_data_list, columns=data_property)
        # timetag_data_df.set_index("account_id", inplace=True)
        # print(timetag_data_df)
        values.append(timetag_data_df)
    all_data = pd.concat(values, keys=Environment.benchmark_index)
    millisecond_timetag = int(time.time() * 1000)
    all_data.to_csv(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:][:-3] + "_" + data_type + millisecond_timetag + ".csv")

    pass


if __name__ == "__main__":
    aaa = EmptyClass()
    aa = copy.deepcopy(aaa)
    if "__slotnames__" in dir(copy.deepcopy(aaa)):
        print("nice")
    else:
        print(dir(aa))
