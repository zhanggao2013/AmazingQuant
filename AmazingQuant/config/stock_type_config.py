# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/20
# @Author  : gao
# @File    : stock_type_config.py
# @Project : AmazingQuant
# ------------------------------


"""
base_type: 基础类型，包含同一市场
extra_type: 扩展类型，包含跨市场
"""
stock_type_info = {
    "base_type": {
        "MARKET_SH": [r"\d{6}.SH"],  # 沪市
        "MARKET_SZ": [r"\d{6}.SZ"],  # 深市
        "MARKET_ZJ": [r"\d{6}.IF", r"\d{5}.IF", r"\d{4}.IF", r"\d{3}.IF"],  # 中金
        "MARKET_SQ": [r"\d{6}.SF", r"\d{5}.SF", r"\d{4}.SF", r"\d{3}.SF"],  # 上期
        "MARKET_DS": [r"\d{6}.DF", r"\d{5}.DF", r"\d{4}.DF", r"\d{3}.DF"],  # 大商
        "MARKET_ZS": [r"\d{6}.ZF", r"\d{5}.ZF", r"\d{4}.ZF", r"\d{3}.ZF"],  # 郑商
        "MARKET_OF": [r"\d{6}.OF"],  # 开放基金
        "MARKET_OP": [r"\d{8}.SHO"],  # 股票期权
        "MARKET_NEW3BOARD": [r"\d{6}.NEEQ"],  # 新三板
        "MARKET_SGT": [r"\d{5}.SGT"],  # 深港通
        "MARKET_HGT": [r"\d{5}.HGT"],  # 沪港通

        "SH_A": [r"60\d{4}.SH", r"688\d{3}.SH"],  # 沪市A股
        "SH_B": [r"90\d{4}.SH"],  # 沪市B股
        "SH_ETF": [r"510\d{3}.SH", r"511\d{3}.SH", r"512\d{3}.SH", r"513\d{3}.SH", r"518\d{3}.SH"],  # 沪市ETF
        "SH_GOVERNMENT_LOAN_REPURCHASE_IMPAWN": [r"204\d{3}.SH"],  # 沪市质押式国债回购

        "SZ_A": [r"00\d{4}.SZ", r"30\d{4}.SZ"],  # 深市A股
        "SZ_B": [r"20\d{4}.SZ"],  # 深市B股
        "SZ_GEM_BORAD": [r"30\d{4}.SZ"],  # 深市创业板
        "SZ_ETF": [r"159\d{3}.SZ"],  # 深市ETF
        "SZ_GLRA": [r"131\d{3}.SZ"],  # 沪市质押式国债回购
    },
    "extra_type": {
        "EXTRA_STOCK_A": ["SH_A", "SZ_A"],  # 沪深A股
    }

}