# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/19
# @Author  : gao
# @File    : update_kline.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime
from multiprocessing import Pool, Manager, cpu_count

import pandas as pd
from mongoengine.context_managers import switch_collection

from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.utils.mongo_connection_me import MongoConnect
from apps.server.database_server.database_field.field_a_share_kline import Kline
from AmazingQuant.data_center.api_data.get_calender import GetCalendar
from AmazingQuant.data_center.api_data.get_collection_list import GetCollectionList
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.utils.performance_test import Timer
from AmazingQuant.utils.security_type import is_security_type


class UpdateKlineData(object):
    def __init__(self):
        self.field = ['time_tag', 'open', 'high', 'low', 'close', 'volume', 'amount', 'match_items', 'interest']
        self.end = ''
        self.calendar_SZ = []

    def get_all_market_data(self, security_list, end=datetime.now()):
        """

        :param security_list:
        :param end:
        :return:
        """
        calendar_obj = GetCalendar()
        self.calendar_SZ = calendar_obj.get_calendar('SZ')
        self.end = end
        database = DatabaseName.A_SHARE_KLINE_DAILY.value
        process_num = cpu_count()+2
        process_stock_num = int(len(security_list) / process_num) + 1
        security_list_split = []
        for i in range(int(len(security_list) / process_stock_num)):
            if i < int(len(security_list) / process_stock_num)-1:
                security_list_split.append(security_list[i * process_stock_num: (i + 1) * process_stock_num])
            else:
                security_list_split.append(security_list[i * process_stock_num:])

        with Manager() as manager:
            process_pool = Pool(process_num)
            process_manager_dict = manager.dict()
            for security_list_i in range(len(security_list_split)):
                process_pool.apply_async(self._get_data_with_process_pool,
                                         args=(database, security_list_split[security_list_i], process_manager_dict, security_list_i))
            process_pool.close()
            process_pool.join()
            process_dict = dict(process_manager_dict)
            stock_data_dict = {}
            for single_stock_data in process_dict.values():
                stock_data_dict.update(single_stock_data)

            field_data_dict = {}
            for i in self.field:
                if i != 'time_tag':
                    field_data_pd = pd.DataFrame({key: value[i] for key, value in stock_data_dict.items()})
                    # 原始数据的开高低收除以10000
                    if i in ['open', 'high', 'low', 'close']:
                        field_data_dict[i] = field_data_pd.div(10000)
                    else:
                        field_data_dict[i] = field_data_pd
            return field_data_dict

    def _get_data_with_process_pool(self, database, security_list, process_manager_dict, security_list_i):
        with MongoConnect(database):
            thread_data_dict = {}
            for stock in security_list:
                with switch_collection(Kline, stock) as KlineDaily_security_code:
                    security_code_data = KlineDaily_security_code.objects(time_tag__lte=self.end).as_pymongo()
                    security_code_data_df = pd.DataFrame(list(security_code_data)).reindex(columns=self.field)
                    security_code_data_df.set_index(["time_tag"], inplace=True)
                    thread_data_dict[stock] = security_code_data_df.reindex(self.calendar_SZ).fillna(method='ffill')
                    if stock=='003816.SZ':
                        print(stock, thread_data_dict[stock])
            process_manager_dict[security_list_i] = thread_data_dict

    def update_all_market_data(self, end=datetime.now()):
        get_collection_list = GetCollectionList()
        a_share_list = get_collection_list.get_a_share_list()
        a_share_list = [i for i in a_share_list if is_security_type(i, 'EXTRA_STOCK_A')]
        all_market_data = self.get_all_market_data(security_list=a_share_list, end=end)
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.A_SHARE.value
        for field in self.field:
            if field not in ['time_tag', 'interest']:
                path = LocalDataPath.path + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
                data_name = field
                data = pd.DataFrame(all_market_data[field])
                print(data['003816.SZ'])
                data.to_csv(path+data_name+'.csv')
                save_data_to_hdf5(path, data_name, data)


    def update_index_data(self, end=datetime.now()):
        """

        :param end:
        :return:
        """
        get_collection_list = GetCollectionList()
        index_list = get_collection_list.get_index_list()
        self.end = end
        database = DatabaseName.INDEX_KLINE_DAILY.value
        with MongoConnect(database):
            index_data_dict = {}
            for index_code in index_list:
                with switch_collection(Kline, index_code) as KlineDaily_index_code:
                    security_code_data = KlineDaily_index_code.objects(time_tag__lte=self.end).as_pymongo()
                    security_code_data_df = pd.DataFrame(list(security_code_data)).reindex(columns=self.field)
                    security_code_data_df.set_index(["time_tag"], inplace=True)
                    # 数据库中数据多了一天，特殊处理删除了
                    if pd.Timestamp(datetime(2016, 1, 1)) in security_code_data_df.index:
                        security_code_data_df = security_code_data_df.drop(labels=datetime(2016, 1, 1), axis=0)
                    index_data_dict[index_code] = security_code_data_df
        field_data_dict = {}
        for i in self.field:
            if i != 'time_tag':
                field_data_pd = pd.DataFrame({key: value[i] for key, value in index_data_dict.items()})
                # 原始数据的开高低收除以10000
                if i in ['open', 'high', 'low', 'close']:
                    field_data_dict[i] = field_data_pd.div(10000)
                else:
                    field_data_dict[i] = field_data_pd
        folder_name = LocalDataFolderName.MARKET_DATA.value
        sub_folder_name = LocalDataFolderName.KLINE_DAILY.value
        sub_sub_folder_name = LocalDataFolderName.INDEX.value
        for field in self.field:
            if field not in ['time_tag', 'interest']:
                path = LocalDataPath.path + folder_name + '/' + sub_folder_name + '/' + sub_sub_folder_name + '/'
                data_name = field
                save_data_to_hdf5(path, data_name, pd.DataFrame(field_data_dict[field]))


if __name__ == '__main__':
    with Timer(True):
        kline_object = UpdateKlineData()
        kline_object.update_all_market_data()
        # kline_object.update_index_data()
