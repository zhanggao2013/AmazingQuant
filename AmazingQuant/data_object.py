# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : data_object.py.py
# @Project : AmazingQuant
# ------------------------------
from AmazingQuant.constant import Empty

order_data = {  # 代码编号相关
    'account_id': Empty.EMPTY_STRING.value,  # 资金账号
    'order_id': Empty.EMPTY_STRING.value,  # 订单编号
    'instrument': Empty.EMPTY_STRING.value,  # 合约代码
    'exchange': Empty.EMPTY_STRING.value,  # 交易所代码

    # 　报单相关
    'price_type': Empty.EMPTY_STRING.value,  # 报单类型
    'order_price': Empty.EMPTY_FLOAT.value,  # 报单价格
    'direction': Empty.EMPTY_STRING.value,  # 报单方向，期货用
    'offset': Empty.EMPTY_STRING.value,  # 报单开平
    'total_volume': Empty.EMPTY_INT.value,  # 报单总数量
    'deal_volume': Empty.EMPTY_INT.value,  # 报单成交数量
    'status': Empty.EMPTY_STRING.value,  # 报单状态

    'order_time': Empty.EMPTY_STRING.value,  # 发单时间
    'cancel_time': Empty.EMPTY_STRING.value,  # 撤单时间

    # 　CTP相关
    'frond_id': Empty.EMPTY_STRING.value,  # 前置机编号，真实交易用
    'session_id': Empty.EMPTY_STRING.value}  # 连接编号

deal_data = {
    # 　代码编号相关
    'account_id': Empty.EMPTY_STRING.value,  # 资金账号
    'trade_id': Empty.EMPTY_STRING.value,  # 成交编号
    'instrument': Empty.EMPTY_STRING.value,  # 合约代码
    'exchange': Empty.EMPTY_STRING.value,  # 交易所代码
    'order_id': Empty.EMPTY_STRING.value,  # 订单编号

    # 　成交相关
    'deal_price': Empty.EMPTY_FLOAT.value,  # 成交价格
    'direction': Empty.EMPTY_STRING.value,  # 成交方向，期货用
    'offset': Empty.EMPTY_STRING.value,  # 成交开平
    'deal_volume': Empty.EMPTY_INT.value,  # 成交数量
    'deal_time': Empty.EMPTY_STRING.value,  # 成交时间
}

position_data = {
    # 　代码编号相关
    'instrument': Empty.EMPTY_STRING.value,  # 合约代码
    'exchange': Empty.EMPTY_STRING.value,  # 交易所代码
    'account_id': Empty.EMPTY_STRING.value,  # 资金账号

    # 　持仓相关
    'average_price': Empty.EMPTY_FLOAT.value,  # 持仓均价
    'direction': Empty.EMPTY_STRING.value,  # 持仓方向，期货用
    'position': Empty.EMPTY_INT.value,  # 持仓数量
    'frozen': Empty.EMPTY_INT.value,  # 冻结数量
    'yesterday_position': Empty.EMPTY_INT.value,  # 昨持仓数量，期货用
    'position_profit': Empty.EMPTY_FLOAT.value,  # 持仓盈亏

    'close': Empty.EMPTY_FLOAT.value,  # 当前bar的收盘价
    'hold_value': Empty.EMPTY_FLOAT.value,  # 持仓市值

}

account_data = {
    # 账号代码相关
    'account_id': Empty.EMPTY_STRING.value,  # 资金账号代码

    # 数值相关
    'pre_balance': Empty.EMPTY_FLOAT.value,  # 昨日账户总资产，期货用
    'total_balance': Empty.EMPTY_FLOAT.value,  # 账户总资产
    'available': Empty.EMPTY_FLOAT.value,  # 可用资金
}

