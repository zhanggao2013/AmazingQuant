# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/22
# @Author  : gao
# @File    : save_data.py
# @Project : AmazingQuant 
# ------------------------------
import os
import pickle


def save_data_to_hdf5(path, data_name, input_data, is_append=False):
    if not os.path.exists(path):
        os.makedirs(path)
    input_data.to_hdf(path + data_name + '.h5', key=data_name, mode='w', append=is_append)


def save_data_to_pkl(path, data_name, input_data={}):
    if not os.path.exists(path):
        os.makedirs(path)
    # 将字典保存到本地文件
    with open(path + data_name + '.pkl', 'wb') as f:
        pickle.dump(input_data, f)


def get_data_to_pkl(path, data_name):
    # 从本地文件加载字典
    with open(path + data_name + '.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
    return loaded_dict
