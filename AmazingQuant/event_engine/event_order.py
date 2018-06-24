# -*- coding: utf-8 -*-

__author__ = "gao"

from AmazingQuant.event_engine.event_engine_base import Event
from AmazingQuant.environment import Environment
from AmazingQuant.constant import *


class EventOrder(Event):
    def __init__(self):
        super().__init__(event_type=EventType.EVENT_ORDER.value)

    @classmethod
    def integer_conversion(cls, event):
        """
        交易数量根据手数取整
        :param event:
        :return:
        """
        Environment.current_order_data.total_volume = 100 * int(Environment.current_order_data.total_volume / 100)

    @classmethod
    def account_available_check(cls, event):
        """
        开仓前　买入资金检查，若不足，则委托状态改为withdraw
        :param event:
        :return:
        """
        trade_balance = Environment.current_order_data.total_volume * Environment.current_order_data.order_price
        if Environment.current_order_data.offset == Offset.OPEN.value:
            for account_data in Environment.bar_account_data_list:
                if account_data.account_id == Environment.current_order_data.session_id:
                    if trade_balance > account_data.available:
                        Environment.current_order_data.status = Status.WITHDRAW.value
                        print("Insufficient Available Capital")

    @classmethod
    def position_available_volume_check(cls, event):
        if Environment.current_order_data.offset == Offset.CLOSE.value:
            num = 0
            if Environment.bar_position_data_list:
                for position_data in Environment.bar_position_data_list:
                    num += 1
                    # 根据资金账号限制卖出数量
                    for account_data in Environment.bar_account_data_list:
                        if account_data.account_id == Environment.current_order_data.session_id:

                            if Environment.current_order_data.instrument + "." + Environment.current_order_data.exchange == \
                                    position_data.instrument + "." + position_data.exchange:
                                if Environment.current_order_data.total_volume > (
                                        position_data.position - position_data.frozen):
                                    print("Insufficient Available Position")
                                    Environment.current_order_data.status = Status.WITHDRAW.value
                                    break
                    # 如果遍历完持仓，没有此次平仓的持仓，Status改为WITHDRAW
                    if num == len(Environment.bar_position_data_list):
                        print("Insufficient Available Position")
                        Environment.current_order_data.status = Status.WITHDRAW.value
                        break
            # 如果持仓为空，Status改为WITHDRAW
            else:
                print("Insufficient Available Position")
                Environment.current_order_data.status = Status.WITHDRAW.value

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
