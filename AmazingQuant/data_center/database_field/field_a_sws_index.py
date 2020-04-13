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
    # 时间戳
    time_tag = DateTimeField(required=True)
    # 昨收
    pre_close = FloatField(required=True)
    # 开
    open = FloatField(required=True)
    # 高
    high = FloatField(required=True)
    # 低
    low = FloatField(required=True)
    # 收
    close = FloatField(required=True)
    # 成交量(百股)
    volume = FloatField(required=True)
    # 成交金额(千元)
    amount = FloatField(required=True)

    # 指数市盈率
    index_pe = FloatField(required=True)

    # 指数市净率
    index_pb = FloatField(required=True)

    # A股流通市值(万元)
    index_free_float_market_capitalisation = FloatField(required=True)

    # 总市值(万元)
    index_total_market_capitalisation = FloatField(required=True)

    meta = {'indexes': ['time_tag'], 'shard_key': ('time_tag',)}
    # # 指数Wind代码
    # S_INFO_WINDCODE
    # # 交易日期
    # TRADE_DT
    # # 昨收盘价
    # S_DQ_PRECLOSE
    # # 开盘价
    # S_DQ_OPEN
    #
    # # 最高价
    # S_DQ_HIGH
    #
    # # 最低价
    # S_DQ_LOW
    #
    # # 收盘价
    # S_DQ_CLOSE
    #
    # # 成交量(百股)
    # S_DQ_VOLUME
    #
    # # 成交金额(千元)
    # S_DQ_AMOUNT
    #
    # # 指数市盈率
    # S_VAL_PE
    #
    # # 指数市净率
    # S_VAL_PB
    #
    # # A股流通市值(万元)
    # S_DQ_MV
    #
    # # 总市值(万元)
    # S_VAL_MV
