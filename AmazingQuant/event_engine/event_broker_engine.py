# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_broker_engine.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.trade_center.event_deal import EventDeal
from AmazingQuant.environment import Environment


def run_broker_engine(strategy):
    """
    deal 交易撮合，更新　OrderData DealData AccountData PositionData
    OrderData(返回状态：已成　已撤（检查可用资金　可用数量不合格）等)
    :param new_order_data:
    :return:
    """
    event_deal = EventDeal()
    event_deal.event_data_dict["strategy_data"] = strategy
    EventDeal.initialize_deal_data(event_deal)
    EventDeal.slippage_calculate(event_deal)
    EventDeal.commission_calculate(event_deal)
    EventDeal.update_position_list(event_deal)
    EventDeal.update_account_list(event_deal)
    Environment().refresh_current_data(event_deal)

