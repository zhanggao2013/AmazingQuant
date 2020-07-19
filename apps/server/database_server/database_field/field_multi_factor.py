# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/7/18
# @Author  : gao
# @File    : field_multi_factor.py
# @Project : AmazingQuant
# ------------------------------
"""
单因子检测数据保存到mongo
"""
from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField, DictField


class FactorPreProcessingData(Document):
    """
    因子预处理之后的数据
    """
    # 因子名字
    factor_name = StringField(required=True)
    # 因子数据时间戳
    time_tag = DateTimeField(required=True)
    # 因子数据，key：股票代码，value：因子值
    factor_data = DictField(required=True)

    meta = {'indexes': ['factor_name', 'time_tag', ('factor_name', 'time_tag')], 'shard_key': ('factor_name',)}


class FactorIcAnalysisResult(Document):
    """
    因子ic分析结果
    """
    # 因子名字
    factor_name = StringField(required=True)
    # 因子数据开始时间
    begin_date = DateTimeField(required=True)
    # 因子数据结束时间
    end_date = DateTimeField(required=True)
    # IC信号衰减计算，index 是时间序列， columns是decay周期，[1, self.ic_decay], 闭区间
    ic = DictField()
    # p值信号衰减计算，index 是时间序列， columns是decay周期，[1, self.ic_decay], 闭区间
    p_value = DictField()
    # ic分析结果, index如下，column是decay周期，[1, self.ic_decay], 闭区间
    # IC均值、 IC标准差、 IC_IR比率、 IC > 0 占比、 | IC | > 0.02 占比(绝对值)、 偏度、 峰度、
    # 正相关显著比例、负相关显著比例、状态切换比例、同向比例
    # ['ic_mean', 'ic_std', 'ic_ir', 'ic_ratio', 'ic_abs_ratio', 'ic_skewness', 'ic_kurtosis',
    # 'ic_positive_ratio', 'ic_negative_ratio', 'ic_change_ratio', 'ic_unchange_ratio', ]
    ic_result = DictField()

