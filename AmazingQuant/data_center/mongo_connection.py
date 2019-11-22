# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : mongo_connection.py
# @Project : AmazingQuant 
# ------------------------------

import sys
import traceback

from mongoengine import connection
import pymongo

from AmazingQuant.data_center.singleton import singleton
from AmazingQuant.config.database_info import MongodbConfig


@singleton
class MongoConnect(object):
    def __init__(self, database, database_alias="AmazingQuant"):
        self.alias = database_alias
        self.database = database
        try:
            self.conn = pymongo.MongoClient(MongodbConfig.host, MongodbConfig.port)
            self.username = MongodbConfig.username
            self.password = MongodbConfig.password
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
            # 检查是否连接成功
            if not self.connected:
                raise NameError('Status: Connected Error')
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)

    def __enter__(self):
        connection.connect(db=self.database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        print("AmazingQuant Database Connect")

    def __exit__(self, *args):
        connection.disconnect()
        print("AmazingQuant Database Disconnect")

    def connect_db(self, db_name):
        db = self.conn[db_name]
        return db


if __name__ == '__main__':
    # 分片建表
    database = "test"

    with MongoConnect(database):
        print("done")

    collection_name = "kline_daily00"
    my_conn = MongoConnect(database)
    db = my_conn.connect_db(collection_name)
    # # 激活数据库分片功能
    db_admin = my_conn.connect_db("admin")
    # db_admin.command('enablesharding', database)
    # # 为集合开启分片
    # db_admin.command('shardcollection', database + '.' + collection_name, key={'_id': 1})
