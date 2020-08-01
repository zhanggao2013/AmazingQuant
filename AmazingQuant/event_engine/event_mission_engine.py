# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_mission_engine.py.py
# @Project : AmazingQuant
# ------------------------------


from AmazingQuant.event_engine.event_engine_base import EventEngineBase
from AmazingQuant.trade_center.event_order import *
from AmazingQuant.trade_center.event_risk_management import *


def run_mission_engine(strategy):
    """
    order  和　risk management 两个事件, ,同样使用event_engine,本地计算的engine,重新隔离出一个engine
    在risk management
    更新　OrderData,的状态：已报
    :param order_data:
    :return:
    """
    mission_engine = EventEngineBase()

    event_order = EventOrder()
    mission_engine.put(event_order)

    mission_engine.register(EventType.EVENT_ORDER.value, EventOrder.integer_conversion)
    mission_engine.register(EventType.EVENT_ORDER.value, EventOrder.account_available_check)
    mission_engine.register(EventType.EVENT_ORDER.value, EventOrder.position_available_volume_check)

    event_risk_management = EventRiskManagement()
    event_risk_management.event_data_dict["strategy"] = strategy
    mission_engine.put(event_risk_management)

    mission_engine.register(EventType.EVENT_RISK_MANAGEMENT.value, EventRiskManagement.black_namelist_check)
    mission_engine.register(EventType.EVENT_RISK_MANAGEMENT.value, EventRiskManagement.change_order_status)
    mission_engine.register(EventType.EVENT_RISK_MANAGEMENT.value, EventRiskManagement.send_order)

    mission_engine.start()
    mission_engine.stop()


if __name__ == '__main__':
    import time

    for i in range(1000):
        time1 = time.time()
        run_mission_engine('qwe')
        time2 = time.time()
        print((time2-time1)*1000)

