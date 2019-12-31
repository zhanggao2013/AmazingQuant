# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/22
# @Author  : gao
# @File    : save_data.py
# @Project : AmazingQuant 
# ------------------------------
import os


def save_data_to_hdf5(path, data_name, input_data, is_append=False):
    if not os.path.exists(path):
        os.mkdir(path)
    input_data.to_hdf(path + data_name + '.h5', key=data_name, mode='w', append=is_append)


