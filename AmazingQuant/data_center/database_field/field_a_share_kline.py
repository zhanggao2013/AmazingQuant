# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/23
# @Author  : gao
# @File    : field_a_share_kline.py
# @Project : AmazingQuant 
# ------------------------------


from datetime import datetime

from mongoengine import Document
from mongoengine.fields import IntField, DateTimeField


class Kline(Document):
    """
    日线行情
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 时间戳
    time_tag = DateTimeField(required=True)
    # 开
    open = IntField(required=True)
    # 高
    high = IntField(required=True)
    # 低
    low = IntField(required=True)
    # 收
    close = IntField(required=True)
    # 成交量
    volume = IntField(required=True)
    # 成交额
    amount = IntField(required=True)
    # 成交笔数
    match_items = IntField(required=True)
    # 持仓量(期货)、IOPV(基金)、利息(债券)
    interest = IntField(required=True)

    meta = {'indexes': ['time_tag'], 'shard_key': ('time_tag',)}
