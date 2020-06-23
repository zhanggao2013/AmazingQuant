# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/6/22
# @Author  : gao
# @File    : redis_test.py
# @Project : AmazingQuant
# ------------------------------

import redis   # 导入redis 模块

r = redis.Redis(host='localhost', port=6378, db=20,decode_responses=True)
r.set('name1', 'runoob1')  # 设置 name 对应的值
print(r['name1'])
print(r.get('name1'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型