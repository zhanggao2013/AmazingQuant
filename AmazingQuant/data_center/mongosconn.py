# -*- coding: utf-8 -*-

__author__ = "gao"

import sys
import traceback
import pymongo

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 40001,
    'db_name': None,
    'username': None,
    'password': None
}



class Singleton(object):
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class MongoConn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.username = MONGODB_CONFIG['username']
            self.password = MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
            # 检查是否连接成功
            if not self.connected:
                raise NameError('stat:connected Error')
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)

    def connect_db(self, db_name):
        db = self.conn[db_name]
        return db

    def check_connected(self):
        # 检查是否连接成功
        if not self.connected:
            raise NameError('stat:connected Error')

    def save(self, db_name, table, value):
        # 一次操作，根据‘_id’是否存在，决定插入或更新记录
        try:
            db = self.conn[db_name]
            db[table].save(value)
        except Exception:
            print(traceback.format_exc())

    def insert(self, db_name, table, value):
        # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
        try:
            db = self.conn[db_name]
            db[table].insert(value, continue_on_error=True)
        except Exception:
            print(traceback.format_exc())

    def update(self, db_name, table, conditions, value, s_upsert=False, s_multi=False):
        try:
            db = self.conn[db_name]
            db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
        except Exception:
            print(traceback.format_exc())

    def upsert_many(self, db_name, table, datas):
        # 批量更新插入，根据‘_id’更新或插入多条记录。
        # 把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
        # 如果更新的字段在mongo中不存在，则直接新增一个字段
        try:
            db = self.conn[db_name]
            bulk = db[table].initialize_ordered_bulk_op()
            for data in datas:
                _id = data['_id']
                bulk.find({'_id': _id}).upsert().update({'$set': data})
            bulk.execute()
        except Exception:
            print(traceback.format_exc())

    def upsert_one(self, db_name, table, data):
        # 更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
        try:
            query = {'_id': data.get('_id', '')}
            db = self.conn[db_name]
            if not db[table].find_one(query):
                db[table].insert(data)
            else:
                data.pop('_id')  # 删除'_id'键
                db[table].update(query, {'$set': data})
        except Exception:
            print(traceback.format_exc())

    def find_one(self, db_name, table, value):
        # 根据条件进行查询，返回一条记录
        try:
            db = self.conn[db_name]
            return db[table].find_one(value)
        except Exception:
            print(traceback.format_exc())

    def find(self, db_name,table, value):
        # 根据条件进行查询，返回所有记录
        try:
            db = self.conn[db_name]
            return db[table].find(value)
        except Exception:
            print(traceback.format_exc())

    def select_colum(self, db_name, table, value, colum):
        # 查询指定列的所有值
        try:
            db = self.conn[db_name]
            return db[table].find(value, colum)
        except Exception:
            print(traceback.format_exc())

if __name__ == "__main__":
    db_name = "market_data_daily"
    collection_name = "test"
    my_conn = MongoConn()
    db = my_conn.connect_db(db_name)
    # 激活数据库分片功能
    db_admin = my_conn.connect_db('admin')
    db_admin.command('enablesharding', db_name)
    # 为集合开启分片
    db_admin.command('shardcollection', db_name + '.' + collection_name, key={'_id': 1})

    datas = [
        {'data': 12},
        {'data': 22},
        {'data': 'cc'}
    ]
    # 插入数据，'mytest'是上文中创建的表名
    # db["test0"].insert(datas)
    my_conn.insert(db_name, collection_name, datas)
    # 查询数据，'mytest'是上文中创建的表名
    res = my_conn.find(db_name, collection_name, {})
    for k in res:
        print(k)
