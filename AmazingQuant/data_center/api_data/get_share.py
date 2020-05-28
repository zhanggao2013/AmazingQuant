# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/28
# @Author  : gao
# @File    : get_share.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath


class GetShare(object):
    def __init__(self):
        self.share_data = pd.DataFrame.empty

    def get_share(self, field=None):
        """

        :param field: 'total_share', 'float_a_share', 'total_share_value',  'float_a_share_value'
        :return:
        """
        if field is None:
            field = 'total_share'
        folder_name = LocalDataFolderName.INDICATOR_EVERYDAY.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = field + '.h5'
        self.share_data = pd.read_hdf(path + data_name)
        return self.share_data


if __name__ == '__main__':
    share_data_obj = GetShare()
    share_data = share_data_obj.get_share()
