# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/1/3
# @Author  : gao
# @File    : get_collection_list.py
# @Project : AmazingQuant
# ------------------------------

from AmazingQuant.utils.mongo_connection_pm import MongoConnectPm
from AmazingQuant.constant import DatabaseName
from AmazingQuant.utils.stock_type import is_stock_type


class GetCollectionList(object):
    def __init__(self):
        self.connect = MongoConnectPm()

    def get_a_share_list(self):
        database_name = DatabaseName.A_SHARE_KLINE_DAILY.value
        a_share_list = self.connect.get_list_collection_names(database_name)
        a_share_list = [i for i in a_share_list if is_stock_type(i, 'EXTRA_STOCK_A')]
        self.connect.disconnect()
        return a_share_list

    def get_index_list(self):
        database_name = DatabaseName.INDEX_KLINE_DAILY.value
        index_list = self.connect.get_list_collection_names(database_name)
        self.connect.disconnect()
        return index_list


if __name__ == '__main__':
    get_collection_list = GetCollectionList()
    a_share_list = get_collection_list.get_a_share_list()
    print(a_share_list)
    index_list = get_collection_list.get_index_list()
    print(index_list)
