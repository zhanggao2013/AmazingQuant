# -*- coding: utf-8 -*-

__author__ = "gao"

import time


def millisecond_to_date(millisecond, format):
    return time.strftime(format, time.localtime(millisecond/1000))


def date_to_millisecond(date="20100101", format='%Y%m%d'):
    return int(time.mktime(time.strptime(date, format))*1000)


def date_str_to_int(date="2010-01-01"):
    return int(date.replace("-", ""))


if __name__ == "__main__":
    print(date_str_to_int(date="2010-01-01"))