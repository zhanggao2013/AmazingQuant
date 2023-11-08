# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/30
# @Author  : gao
# @File    : get_data.py
# @Project : AmazingQuant
# ------------------------------
import pandas as pd


def get_local_data(path, data_name):
    return pd.read_hdf(path + data_name)