# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : field_a_share_indicator_daily.py
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime

from mongoengine import Document
from mongoengine.fields import DictField, DateTimeField, ListField


class AShareIndicatorDaily(Document):
    """
    K线
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 时间戳
    time_tag = DateTimeField(required=True)
    security_code_list = ListField(required=True)
    # 指标数据，key：security_code
    data = ListField(required=True)

    meta = {'indexes': ['time_tag']}
