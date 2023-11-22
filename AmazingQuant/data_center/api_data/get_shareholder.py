# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/11/22
# @Author  : gao
# @File    : get_shareholder.py 
# @Project : AmazingQuant 
# ------------------------------
import pandas as pd

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data


class GetShareholder(object):
    def __init__(self):
        self.shareholder_data = pd.DataFrame.empty

    def get_shareholder(self, holder_type='shareholder'):
        """
        :param holder_type: 'shareholder', 十大股东, 'floatshareholder', 十大流通股东,
        :return:
        """
        folder_name = LocalDataFolderName.FINANCE.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = holder_type + '.h5'
        self.shareholder_data = get_local_data(path, data_name)
        return self.shareholder_data


if __name__ == '__main__':
    shareholder_obj = GetShareholder()
    shareholder_data = shareholder_obj.get_shareholder('shareholder')
    floatshareholder_data = shareholder_obj.get_shareholder('floatshareholder')
