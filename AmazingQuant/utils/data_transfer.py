# -*- coding: utf-8 -*-

__author__ = "gao"

import time


def millisecond_to_date(millisecond, format):
    return time.strftime(format, time.localtime(millisecond))


def date_to_millisecond(date="20100101", format='%Y%m%d'):
    return int(time.mktime(time.strptime(date, format)))


def date_str_to_int(date=""):
    return int(date.replace("-", ""))
