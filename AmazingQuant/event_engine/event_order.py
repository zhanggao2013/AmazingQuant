# -*- coding: utf-8 -*-

__author__ = "gao"

from datetime import datetime

from AmazingQuant.event_engine.event_engine_base import EventEngineBase, Event
from AmazingQuant.constant import EventType, ID
from AmazingQuant.environment import Environment


class EventOrder(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_ORDER.value)

    @classmethod
    def integer_conversion(cls, event):
        Environment.current_order_data.total_volume = 100 * int(Environment.current_order_data.total_volume/100)

    @classmethod
    def account_avaliable_check(cls, event):
        pass

    @classmethod
    def position_avaliable_volume_check(cls, event):
        pass






        """
        回测中：
        读取event.event_data_dict["data"]
        计算后写进environment,save 该事件的records(不需要refresh)
        下一个事件读取　environment，计算后再写进environment,save 该事件的records(不需要refresh)
        所有事件完成后　refresh environment, save all_records to csv
        
        实盘中：
        读取event.event_data_dict["data"]
        计算后写进environment,save 该事件的records(不需要refresh)，
        过risk management,＂写进environment＂改为发送订单请求，从broker定时订阅(从event_engine 的定时器任务订阅),save 该事件的records　
        deal position 都同上　＂订阅＂　并save
        """




