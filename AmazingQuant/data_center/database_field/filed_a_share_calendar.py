# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/11
# @Author  : gao
# @File    : filed_a_share_calendar.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import ListField, DateTimeField, StringField


class AShareCalendar(Document):
    """
    K线
    """
    # 更新时间
    update_date = DateTimeField(default=datetime.utcnow())
    # 市场，SH:上海交易所 SZ:深圳交易所 SHN:沪股通 SZN:深股通
    market = StringField(required=True)
    # 交易日列表
    trade_days = ListField(required=True)