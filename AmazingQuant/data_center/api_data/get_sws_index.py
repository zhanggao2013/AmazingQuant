# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/14
# @Author  : gao
# @File    : get_sws_index.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd
from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath


class GetSwsIndex(object):
    def __init__(self):
        self.all_sws_index = pd.DataFrame.empty

    def get_all_sws_index(self):
        folder_name = LocalDataFolderName.SWS_INDEX.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = folder_name + '.h5'
        self.all_sws_index = pd.read_hdf(path + data_name).sort_values(by='time_tag')
        return self.all_sws_index

    def get_sws_index(self, sws_index_code):
        return self.all_sws_index[self.all_sws_index.sw_index_code == sws_index_code].reset_index(drop=True)


if __name__ == '__main__':
    sws_index_obj = GetSwsIndex()
    sws_index_obj.get_all_sws_index()
    a = sws_index_obj.get_sws_index('801780.SI')
