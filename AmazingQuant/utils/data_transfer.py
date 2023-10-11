# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : data_transfer.py.py
# @Project : AmazingQuant
__author__ = "gao"

import time
from datetime import datetime


def millisecond_to_date(millisecond, format):
    return time.strftime(format, time.localtime(millisecond / 1000))


def date_to_millisecond(date="20100101", format='%Y%m%d'):
    return int(time.mktime(time.strptime(date, format)) * 1000)


def date_str_to_int(date="2010-01-01"):
    return int(date.replace("-", ""))


def datetime_to_millisecond(datetime_obj=datetime.now()):
    return int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)


def millisecond_to_datetime(millisecond):
    return datetime.fromtimestamp(millisecond / 1000)


def date_to_datetime(date='20090101'):
    return datetime.strptime(date, "%Y%m%d")


def date_second_to_datetime(date='20090101121212'):
    return datetime.strptime(date, "%Y%m%d%H%M%S")


def datetime_to_int(date=datetime.now()):
    return int(date.strftime('%Y%m%d'))


if __name__ == "__main__":
    print(date_str_to_int(date="2010-01-01"))
    a = datetime_to_millisecond()
    b = date_to_datetime()
    print(b)
