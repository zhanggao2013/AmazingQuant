# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/22
# @Author  : gao
# @File    : field_a_share_index_members.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField


class AShareIndexMembers(Document):
    """
    A股指数成分股
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 指数代码
    index_code = StringField(required=True, null=True)
    # 成份股代码
    security_code = StringField(required=True, null=True)
    # 纳入日期
    in_date = StringField(required=True, null=True)
    # 剔除日期
    out_date = StringField(required=True, null=True)
    # 最新标志
    current_sign = StringField(required=True, null=True)

    meta = {'indexes': ['index_code', 'security_code', 'in_date']}
