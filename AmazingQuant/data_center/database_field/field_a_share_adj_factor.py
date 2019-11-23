# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/23
# @Author  : gao
# @File    : field_a_share_adj_factor.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, DateTimeField


class AShareAdjFactor(Document):
    """
    A股复权因子
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 证券代码
    security_code = StringField(required=True, null=True)
    # 除权除息日
    ex_date = DateTimeField(required=True, null=True)
    # 复权因子
    adj_factor = FloatField(required=True)

    meta = {'indexes': ['security_code', 'ex_date']}
