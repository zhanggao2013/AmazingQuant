# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/23
# @Author  : gao
# @File    : field_a_share_kline.py
# @Project : AmazingQuant 
# ------------------------------


from datetime import datetime

from mongoengine import Document
from mongoengine.fields import ListField, DateTimeField


class Kline(Document):
    """
    日线行情
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 时间戳
    time_tag = DateTimeField(required=True)
    # 数据，按照开、高、低、收、成交量、成交额、成交笔数、【持仓量(期货)、IOPV(基金)、利息(债券)】
    data = ListField(required=True)

    meta = {'indexes': ['time_tag'], 'shard_key': ('time_tag',)}
