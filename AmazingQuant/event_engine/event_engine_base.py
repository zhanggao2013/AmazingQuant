# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_engine_base.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.constant import EventType


class Event(object):
    """事件对象"""

    def __init__(self, event_type=None):
        """Constructor"""
        self.event_type = event_type  # 事件类型
        self.event_data_dict = {}  # 字典用于保存具体的事件数据


if __name__ == "__main__":
    aa = TestOne()
    aa.test()
