# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/4
# @Author  : gao
# @File    : multi_factor_constant.py
# @Project : AmazingQuant
# ------------------------------

from enum import Enum, unique


@unique
class ExtremeMethod(Enum):
    STD = 'std'
    MAD = 'mad'
    QUANTILE = 'quantile'
    BOX_PLOT = 'box_plot'


@unique
class ScaleMethod(Enum):
    MIN_MAX = 'min_max'
    Z_SCORE = 'z_score'
    RANK = 'rank'


@unique
class NeutralizeMethod(Enum):
    INDUSTRY = 'industry'
    MARKET_VALUE = 'market_value'

