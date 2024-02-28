# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2024/2/23
# @Author  : gao
# @File    : simulated_index.py 
# @Project : AmazingQuant 
# ------------------------------
import pandas as pd

import os

# 获取当前工作目录
rptdate = '20231231'
current_dir = './etf_stockhold/' + rptdate

etf_hold_detail_dict = {}
proportion_dict = {}
# 遍历当前目录下的所有文件和子目录
for file in os.listdir(current_dir):
    # 判断是否为文件（不包括目录）
    # if os.path.isfile(file):
    #     print(file)
    etf_hold_detail = pd.read_csv(current_dir+'/'+file)
    etf_hold_detail = etf_hold_detail.sort_values(by=['proportiontototalstockinvestments'], ascending=False).iloc[:10, :]

    proportion = etf_hold_detail['proportiontototalstockinvestments'].sum()
    if proportion > 30:
        etf_hold_detail_dict[file[:-4]] = etf_hold_detail

