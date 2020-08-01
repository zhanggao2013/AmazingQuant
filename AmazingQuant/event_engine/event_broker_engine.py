# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_broker_engine.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.event_engine.event_engine_base import EventEngineBase
from AmazingQuant.constant import EventType
from AmazingQuant.trade_center.event_deal import EventDeal
from AmazingQuant.environment import Environment


def run_broker_engine(strategy):
    """
    deal 交易撮合，更新　OrderData DealData AccountData PositionData
    OrderData(返回状态：已成　已撤（检查可用资金　可用数量不合格）等)
    :param new_order_data:
    :return:
    """
    broker_engine = EventEngineBase()
    event_deal = EventDeal()
    event_deal.event_data_dict["strategy_data"] = strategy
    broker_engine.put(event_deal)

    broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.initialize_deal_data)
    broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.slippage_calculate)
    broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.commission_calculate)
    broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.update_position_list)
    broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.update_account_list)
    broker_engine.register(EventType.EVENT_DEAL.value, Environment().refresh_current_data)

    broker_engine.start()
    broker_engine.stop()

