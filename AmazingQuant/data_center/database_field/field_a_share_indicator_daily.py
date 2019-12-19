# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/18
# @Author  : gao
# @File    : field_a_share_indicator_daily.py
# @Project : AmazingQuant 
# ------------------------------
from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, ListField, BinaryField


class AShareIndicatorDaily(Document):
    """
    K线
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 数据开始时间戳
    start_time = DateTimeField(required=True)
    # 数据截止时间戳
    end_time = DateTimeField(required=True)
    # 指标周期
    period = StringField(required=True)
    # 指标数据, dataframe转二进制
    data = BinaryField(required=True)

    meta = {'indexes': ['end_time']}
