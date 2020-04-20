# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/20
# @Author  : gao
# @File    : stock_type.py
# @Project : AmazingQuant
# ------------------------------
import re
from AmazingQuant.config.stock_type_config import stock_type_info


def is_stock_type(stock_code, stock_type):
    type_list = []
    try:
        type_list = stock_type_info["base_type"][stock_type]
    except KeyError:
        try:
            extra_type_list = stock_type_info["extra_type"][stock_type]
            for i in extra_type_list:
                type_list += stock_type_info["base_type"][i]
        except KeyError:
            return False
    for i in type_list:
        if re.match(i, stock_code):
            return True
    return False


if __name__ == '__main__':
    print(is_stock_type("300792.SZ", "SZ_GEM_BORAD"))



