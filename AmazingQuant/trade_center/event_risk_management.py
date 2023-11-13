# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_risk_management.py.py
# @Project : AmazingQuant
# ------------------------------
from datetime import datetime

from AmazingQuant.event_engine.event_engine_base import Event
from AmazingQuant.constant import EventType, Status
from AmazingQuant.environment import Environment


class EventRiskManagement(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_RISK_MANAGEMENT.value)

    @classmethod
    def black_namelist_check(cls, event):
        stock_code = Environment.current_order_data.instrument + "." + Environment.current_order_data.exchange
        if Environment.current_order_data.status == Status.NOT_REPORTED.value and \
                stock_code in Environment.black_namelist:
            Environment.is_pass_risk = False
            Environment.logger.info("Order Stock_code in Black_namelist")
        # Environment.logger.info("black_namelist_check")
        pass

    @classmethod
    def change_order_status(cls, event):
        if Environment.is_pass_risk is False:
            Environment.current_order_data.status = Status.WITHDRAW.value
        pass

    @classmethod
    def send_order(cls, event):
        if Environment.current_order_data.status == Status.NOT_REPORTED.value:
            Environment.current_order_data.status = Status.NOT_TRADED.value
            Environment.current_order_data.order_time = event.event_data_dict["strategy"].time_tag
            Environment.is_send_order = True
        pass

