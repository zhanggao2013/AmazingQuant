# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/7/18
# @Author  : gao
# @File    : field_multi_factor.py
# @Project : AmazingQuant
# ------------------------------
"""
单因子检测数据保存到mongo
"""
from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField, DictField


class FactorPreProcessingData(Document):
    """
    因子预处理之后的数据
    """
    # 因子名字
    factor_name = StringField(required=True)
    # 因子数据时间戳
    time_tag = DateTimeField(required=True)
    # 因子数据，key：股票代码，value：因子值
    factor_data = DictField(required=True)

    meta = {'indexes': ['factor_name', 'time_tag', ('factor_name', 'time_tag')], 'shard_key': ('factor_name',)}

