# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : market_data_daily_to_MongoDB.py
# @Project : AmazingQuant
# ------------------------------


import os
import re
import json
import pandas as pd

from mongosconn import MongoConn
from AmazingQuant.constant import DatabaseName

if __name__ == "__main__":
    db_name = DatabaseName.MARKET_DATA_DAILY.value
    my_conn = MongoConn()
    db = my_conn.connect_db(db_name)
    # 激活数据库分片功能
    db_admin = my_conn.connect_db('admin')
    db_admin.command('enablesharding', db_name)
    path = "./backtest_data/market_data_daily/"
    market_list = ["SH", "SZ"]
    for market in market_list:
        files = os.listdir(path + market)
        for file_num in range(len(files)):
            if not os.path.isdir(files[file_num]):
                print(files[file_num])
                collection_data = pd.read_csv(path + market + "/" + files[file_num], sep=",",
                                              encoding="utf8")
                collection_name = str(re.sub("\D", "", files[file_num])) + "." + market
                print(collection_name)
                # shard key
                db_admin.command('shardcollection', db_name + '.' + collection_name, key={'_id': 1})
                collection_data = collection_data.sort_values(axis=0, ascending=True, by="timetag")
                collection_data_list = json.loads(collection_data.T.to_json()).values()
                collection_data_list_sort = sorted(collection_data_list, key=lambda x: x.__getitem__("timetag"))
                # print(collection_data_list)
                # 插入数据
                if collection_data_list_sort:
                    my_conn.insert(db_name, collection_name, collection_data_list_sort)
