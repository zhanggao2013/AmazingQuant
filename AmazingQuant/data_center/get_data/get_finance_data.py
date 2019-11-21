# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/21
# @Author  : gao
# @File    : get_finance_data.py
# @Project : AmazingQuant
# ------------------------------

from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.data_center.database_field.field_finance_data import AShareIncome, AShareCashFlow
from AmazingQuant.utils.performance_test import Timer


if __name__ == '__main__':
    database = 'stock_base_data'
    with MongoConnect(database):
        with Timer(True):
            security_code_list = AShareCashFlow.objects.distinct('security_code')
            data = AShareCashFlow.objects(security_code__in=security_code_list, statement_type=408009000)
            for i in data:
                print(i.security_code)
