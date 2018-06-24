# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event, EventEngineBase
from AmazingQuant.constant import EventType
from AmazingQuant.event_engine.event_deal import EventDeal
from AmazingQuant.data_object import DealData
from AmazingQuant.environment import Environment


class EventBrokerEngine(object):

    def run_broker(self, strategy):
        """
        deal 交易撮合，更新　OrderData DealData AccountData PositionData
        OrderData(返回状态：已成　已撤（检查可用资金　可用数量不合格）等)
        :param new_order_data:
        :return:
        """
        broker_engine = EventEngineBase()
        event_deal = EventDeal()
        event_deal.event_data_dict["strategy"] = strategy
        broker_engine.put(event_deal)

        broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.initialize_deal_data)
        broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.slippage_calculate)
        broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.commission_calculate)
        broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.update_position_list)
        broker_engine.register(EventType.EVENT_DEAL.value, EventDeal.update_account_list)
        broker_engine.register(EventType.EVENT_DEAL.value, Environment.refresh_current_data)
        broker_engine.start(timer=False)
        broker_engine.stop()

