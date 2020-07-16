# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : pymongo_test.py.py
# @Project : AmazingQuant
# ------------------------------

"""
check 是否启动服务 mongodb
"""


from pymongo import MongoClient
import datetime
conn = MongoClient('127.0.0.1', 40003)
db = conn['market_data_daily']

col_data = db["data_test"]
db_admin = conn['admin']
#db_admin.command('enablesharding', 'market_data_daily')
db_admin.command('shardcollection', 'market_data_daily.data_test', key = {'_id':1})

post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}
new_result = col_data.insert_many([ post_1,post_2,post_3])
scotts_posts = col_data.find({'author': 'Scott'})
for post in scotts_posts:
    print(post)
