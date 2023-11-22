# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/28
# @Author  : gao
# @File    : get_share.py
# @Project : AmazingQuant
# ------------------------------

import pandas as pd

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data


class GetShare(object):
    def __init__(self):
        self.share_data = pd.DataFrame.empty

    def get_share(self, field='total_share'):
        """

        :param field: 'total_share', 'float_a_share', 'total_share_value',  'float_a_share_value'
        :return:
        """
        folder_name = LocalDataFolderName.INDICATOR_EVERYDAY.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = field + '.h5'
        self.share_data = get_local_data(path, data_name)
        return self.share_data


if __name__ == '__main__':
    share_data_obj = GetShare()
    share_data = share_data_obj.get_share('float_a_share_value')
