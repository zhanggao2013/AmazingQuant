# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : factor_preprocessing.py
# @Project : AmazingQuant
# ------------------------------
"""
因子数据预处理
1.去极值
   (1) 3sigma法
   (2) MAD法,Median Absolute Deviation 绝对值差中位数法
   (3) Boxplot法
2.中性化
    市值、行业因子作为解释变量做线性回归,取残差作为新的单因子值
3.补空值(可不做)
    个股所处行业均值
4.标准化
    (1) 最小-最大利差标准化
    (2) Z-score标准化,
    (3) 排序百分位,标准化成均匀分布
"""