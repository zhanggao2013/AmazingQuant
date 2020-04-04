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
    BOX_PLOT = 'box_plot'


