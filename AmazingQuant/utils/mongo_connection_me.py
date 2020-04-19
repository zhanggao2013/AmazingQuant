# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : mongo_connection_me.py
# @Project : AmazingQuant 
# ------------------------------

from mongoengine import connection

from AmazingQuant.utils.singleton import singleton
from AmazingQuant.config.database_info import MongodbConfig


@singleton
class MongoConnect(object):
    def __init__(self, database, database_alias="AmazingQuant"):
        self.alias = database_alias
        self.database = database

    def __enter__(self):
        connection.connect(db=self.database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        print("AmazingQuant Database Connect", self.database)

    def __exit__(self, *args):
        connection.disconnect()
        print("AmazingQuant Database Disconnect", self.database)


if __name__ == '__main__':
    database = "test"
    with MongoConnect(database):
        print("done")
    collection_name = "kline_daily"
    my_conn = MongoConnect(database)
