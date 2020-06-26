# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : data_object.py.py
# @Project : AmazingQuant
# ------------------------------
import json

from AmazingQuant.constant import Empty


class OrderData(object):
    def __init__(self):
        # 　代码编号相关
        self.order_id = Empty.EMPTY_STRING.value  # 订单编号
        self.instrument = Empty.EMPTY_STRING.value  # 合约代码
        self.exchange = Empty.EMPTY_STRING.value  # 交易所代码

        # 　报单相关
        self.price_type = Empty.EMPTY_STRING.value  # 报单类型
        self.order_price = Empty.EMPTY_FLOAT.value  # 报单价格
        self.direction = Empty.EMPTY_STRING.value  # 报单方向，期货用
        self.offset = Empty.EMPTY_STRING.value  # 报单开平
        self.total_volume = Empty.EMPTY_INT.value  # 报单总数量
        self.deal_volume = Empty.EMPTY_INT.value  # 报单成交数量
        self.status = Empty.EMPTY_STRING.value  # 报单状态

        self.order_time = Empty.EMPTY_STRING.value  # 发单时间
        self.cancel_time = Empty.EMPTY_STRING.value  # 撤单时间

        # 　CTP相关
        self.frond_id = Empty.EMPTY_STRING.value  # 前置机编号，真实交易用
        self.session_id = Empty.EMPTY_STRING.value  # 连接编号

    def __str__(self):
        obj_property = {'order_id': self.order_id,
                        'instrument': self.instrument,
                        'exchange': self.exchange,

                        'price_type': self.price_type,
                        'order_price': self.order_price,
                        'direction': self.direction,
                        'offset': self.offset,
                        'total_volume': self.total_volume,
                        'deal_volume': self.deal_volume,
                        'status': self.status,

                        'order_time': self.order_time,
                        'cancel_time': self.cancel_time,

                        'frond_id': self.frond_id,
                        'session_id': self.session_id}
        return json.dumps(obj_property)


class DealData(object):
    def __init__(self):
        # 　代码编号相关
        self.trade_id = Empty.EMPTY_STRING.value  # 成交编号
        self.instrument = Empty.EMPTY_STRING.value  # 合约代码
        self.exchange = Empty.EMPTY_STRING.value  # 交易所代码
        self.order_id = Empty.EMPTY_STRING.value  # 订单编号

        # 　成交相关
        self.deal_price = Empty.EMPTY_FLOAT.value  # 成交价格
        self.direction = Empty.EMPTY_STRING.value  # 成交方向，期货用
        self.offset = Empty.EMPTY_STRING.value  # 成交开平
        self.deal_volume = Empty.EMPTY_INT.value  # 成交数量
        self.deal_time = Empty.EMPTY_STRING.value  # 成交时间

    def __str__(self):
        obj_property = {'trade_id': self.trade_id,
                        'instrument': self.instrument,
                        'exchange': self.exchange,
                        'order_id': self.order_id,

                        'deal_price': self.deal_price,
                        'direction': self.direction,
                        'offset': self.offset,
                        'deal_volume': self.deal_volume,
                        'deal_time': self.deal_time}
        return json.dumps(obj_property)



class PositionData(object):
    def __init__(self):
        # 　代码编号相关
        self.instrument = Empty.EMPTY_STRING.value  # 合约代码
        self.exchange = Empty.EMPTY_STRING.value  # 交易所代码
        self.account_id = Empty.EMPTY_STRING.value  # 资金账号

        # 　持仓相关
        self.average_price = Empty.EMPTY_FLOAT.value  # 持仓均价
        self.direction = Empty.EMPTY_STRING.value  # 持仓方向，期货用
        self.position = Empty.EMPTY_INT.value  # 持仓数量
        self.frozen = Empty.EMPTY_INT.value  # 冻结数量
        self.yesterday_position = Empty.EMPTY_INT.value  # 昨持仓数量，期货用
        self.position_profit = Empty.EMPTY_FLOAT.value  # 持仓盈亏

    def __str__(self):
        obj_property = {'instrument': self.instrument,
                        'exchange': self.exchange,
                        'account_id': self.account_id,

                        'average_price': self.average_price,
                        'direction': self.direction,
                        'position': self.position,
                        'frozen': self.frozen,
                        'yesterday_position': self.yesterday_position,
                        'position_profit': self.position_profit}
        return json.dumps(obj_property)


class AccountData(object):
    def __init__(self):
        # 账号代码相关
        self.account_id = Empty.EMPTY_STRING.value  # 资金账号代码

        # 数值相关
        self.pre_balance = Empty.EMPTY_FLOAT.value  # 昨日账户总资产，期货用
        self.total_balance = Empty.EMPTY_FLOAT.value  # 账户总资产
        self.available = Empty.EMPTY_FLOAT.value  # 可用资金

    def __str__(self):
        obj_property = {'account_id': self.account_id,
                        'pre_balance': self.pre_balance,
                        'total_balance': self.pre_balance,
                        'available': self.pre_balance}
        return json.dumps(obj_property)


if __name__ == '__main__':
    print(json.loads(AccountData().__str__()))
