# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/13
# @Author  : gao
# @File    : field_a_sws_index.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField


class ASwsIndex(Document):
    """
    申万行业指数行情
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 申万指数代码
    sw_index_code = StringField(required=True)
    # 时间戳
    time_tag = DateTimeField(required=True)
    # 昨收
    pre_close = IntField(required=True)
    # 开
    open = IntField(required=True)
    # 高
    high = IntField(required=True)
    # 低
    low = IntField(required=True)
    # 收
    close = IntField(required=True)
    # 成交量(百股)
    volume = IntField(required=True)
    # 成交金额(千元)
    amount = IntField(required=True)

    # 指数市盈率
    index_pe = FloatField(required=True)

    # 指数市净率
    index_pb = FloatField(required=True)

    # A股流通市值(万元)
    index_free_float_market_capitalisation = FloatField(required=True)

    # 总市值(万元)
    index_total_market_capitalisation = FloatField(required=True)

    meta = {'indexes': ['time_tag'], 'shard_key': ('time_tag',)}
