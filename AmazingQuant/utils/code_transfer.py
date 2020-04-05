# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/19
# @Author  : gao
# @File    : code_transfer.py
# @Project : AmazingQuant
# ------------------------------


def market_code_to_code_market(code):
    return code[2:] + '.' + code[:2]


def code_market_to_market_code(code):
    return code[-2:] + code[:6]


if __name__ == '__main__':
    code_market = market_code_to_code_market('SH600000')
    market_code = code_market_to_market_code('600000.SH')
    print(market_code)