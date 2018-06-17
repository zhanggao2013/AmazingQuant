# -*- coding: utf-8 -*-

__author__ = "gao"

import random


def generate_random_id(topic="", lens=8):
    _list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
    num = random.sample(_list, lens)
    return "{}_{}".format(topic, "".join(num))


if __name__ == "__main__":
    print(generate_random_id(topic="aa", lens=8))
