# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/23
# @Author  : gao
# @File    : field_ex_right_dividend.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField


class AExRightDividend(Document):
    """
    A股除权出息
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 证券代码
    security_code = StringField(required=True, null=True)
    # 除权除息日
    ex_date = StringField(required=True, null=True)
    # 除权类型
    ex_type = StringField(required=True, null=True)
    # 除权说明
    ex_description = StringField(required=True, null=True)
    # 派息比例
    cash_dividend_ratio = FloatField(required=True, null=True)
    # 送股比例
    bonus_share_ratio = FloatField(required=True, null=True)
    # 配股比例
    rightsissue_ratio = FloatField(required=True, null=True)
    # 配股价格
    rightsissue_price = FloatField(required=True, null=True)
    # 转增比例
    conversed_ratio = FloatField(required=True, null=True)
    # 增发价格
    seo_price = FloatField(required=True, null=True)
    # 增发比例
    seo_ratio = FloatField(required=True, null=True)
    # 缩减比例
    consolidate_split_ratio = FloatField(required=True, null=True)

    meta = {'indexes': ['security_code', 'ex_date']}
