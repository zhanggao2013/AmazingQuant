# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_mission_engine.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.trade_center.event_order import *
from AmazingQuant.trade_center.event_risk_management import *


def run_mission_engine(strategy):
    """
    order和　risk management 两个事件, 同样使用event_engine,本地计算的engine,重新隔离出一个engine
    在risk management
    更新　OrderData,的状态：已报
    :param order_data:
    :return:
    """
    event_order = EventOrder()
    EventOrder.integer_conversion(event_order)
    EventOrder.account_available_check(event_order)
    EventOrder.position_available_volume_check(event_order)

    event_risk_management = EventRiskManagement()
    event_risk_management.event_data_dict["strategy"] = strategy
    EventRiskManagement.black_namelist_check(event_risk_management)
    EventRiskManagement.change_order_status(event_risk_management)
    EventRiskManagement.send_order(event_risk_management)


if __name__ == '__main__':
    import time

    for i in range(1000):
        time1 = time.time()
        run_mission_engine('qwe')
        time2 = time.time()
        print((time2-time1)*1000)

