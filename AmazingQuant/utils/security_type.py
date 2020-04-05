# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/9
# @Author  : gao
# @File    : security_type.py
# @Project : AmazingQuant 
# ------------------------------

import re
from AmazingQuant.config.security_type_config import security_type_info


def is_security_type(stock_code, security_type):
    type_list = []
    try:
        type_list = security_type_info["base_type"][security_type]
    except KeyError:
        try:
            extra_type_list = security_type_info["extra_type"][security_type]
            for i in extra_type_list:
                type_list += security_type_info["base_type"][i]
        except KeyError:
            return False
    for i in type_list:
        if re.match(i, stock_code):
            return True
    return False


if __name__ == '__main__':
    print(is_security_type("H00914.SH", "EXTRA_STOCK_A"))
