# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/23
# @Author  : gao
# @File    : field_a_share_capitalization.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField


class AShareCapitalization(Document):
    """
    中国A股股本
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 证券代码
    security_code = StringField(required=True, null=True)
    # 变动日期, 备注:上市日期
    change_date = DateTimeField(required=True, null=True)
    # 总股本(万股)
    total_share = FloatField(required=True, null=True)
    # 流通股(万股)  备注:流通A股 +, 流通B股 +, 流通H股 +, 境外流通股
    float_share = FloatField(required=True, null=True)
    # 流通A股(万股), 备注:人民币普通股
    float_a_share = FloatField(required=True, null=True)
    # 流通B股(万股), 备注:以外币计价交易的人民币特种股
    float_b_share = FloatField(required=True, null=True)
    # 流通H股(万股), 备注:大陆注册，香港上市的外资股
    float_h_share = FloatField(required=True, null=True)

