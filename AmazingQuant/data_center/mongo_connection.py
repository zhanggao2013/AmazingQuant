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
    def __init__(self, database_alias="AmazingQuant"):
        self.alias = database_alias
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
        connection.connect(MongodbConfig.db_name, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, alias=self.alias)
        print("AmazingQuant Database Connect")

    def __exit__(self, *args):
        connection.disconnect(alias=self.alias)
        print("AmazingQuant Database Disconnect")

    def connect_db(self, db_name):
        db = self.conn[db_name]
        return db


if __name__ == '__main__':
    with MongoConnect():
        print("done")

    # 分片建表
    db_name = "market_data_daily"
    collection_name = "test"
    my_conn = MongoConnect()
    db = my_conn.connect_db(db_name)
    # 激活数据库分片功能
    db_admin = my_conn.connect_db("admin")
    db_admin.command('enablesharding', db_name)
    # 为集合开启分片
    db_admin.command('shardcollection', db_name + '.' + collection_name, key={'_id': 1})
