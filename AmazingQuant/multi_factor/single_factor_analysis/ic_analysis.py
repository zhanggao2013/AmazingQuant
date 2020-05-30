# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : ic_analysis.py
# @Project : AmazingQuant
# ------------------------------
"""
IC分析
IC是指因子在第T期的因子值与T+1期的股票收益的相关系数
1.计算rank_IC
2.评价指标
    （1） IC均值
    （2） IC标准差
    （3） IC_IR比率
    （4） IC>0占比
    （5） |IC|>0.02占比(绝对值)
    （6） p-value（有效性）,全部都计算时间序列
    （7） IC信号衰减计算
"""
from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class IcAnalysis(object):
    def __init__(self, factor):
        self.factor = factor


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    ic_analysis_obj = IcAnalysis(factor_ma5)
