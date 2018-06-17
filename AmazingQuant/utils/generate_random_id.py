# -*- coding: utf-8 -*-

__author__ = "gao"

import random

from AmazingQuant.constant import ID


def generate_random_id(topic=ID.ACCOUNT_ID.value, lens=8):
    _list = [str(i) for i in range(10)]
    num = random.sample(_list, lens)
    return "{}_{}".format(topic, "".join(num))


if __name__ == "__main__":
    print(generate_random_id(topic=ID.ORDER_ID.value))
