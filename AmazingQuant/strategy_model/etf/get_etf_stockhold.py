# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2024/2/22
# @Author  : gao
# @File    : get_etf_stockhold.py 
# @Project : AmazingQuant 
# ------------------------------
import pandas as pd
from WindPy import w

code_list = list(pd.read_excel('code.xlsx').iloc[:, 0])
code_list = [str(i) + '.SH' if str(i)[0] == '5' else str(i) + '.SZ' for i in code_list]
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功


rptdate = '20231231'
result_dict = {}
for code in code_list:
    result = w.wset("allfundhelddetail", "rptdate=" + rptdate + ";windcode=" + code)
    result_df = pd.DataFrame(result.Data, index=result.Fields).T
    if not result_df.empty:
        result_dict[code] = result_df
        print(code)
        result_df.to_csv('./etf_stockhold/'+ rptdate + '/'+ code+'.csv')


