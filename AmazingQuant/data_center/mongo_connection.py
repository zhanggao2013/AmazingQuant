# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : mongo_connection.py
# @Project : AmazingQuant 
# ------------------------------

from mongoengine import connection

from AmazingQuant.data_center.singleton import singleton

@singleton
class MongoConnect(object):
    def __init__(self, database_alias="Account_Analysis"):
        self.alias = database_alias

    def __enter__(self):
        host = "127.0.0.1"
        port = 40001
        database = "AmazingQuant"
        user = None
        password = None
        connection.connect(database, host=host, port=port, password=password, username=user)
        print("AmazingQuant database connect")

    def __exit__(self, *args):
        connection.disconnect(alias=self.alias)
        print("AmazingQuant database disconnect")


if __name__ == '__main__':

    with MongoConnect():
        print("done")
