# -*- coding: utf-8 -*-

__author__ = "gao"

import pandas as pd

from AmazingQuant.constant import RunMode

class Environment(object):
    run_mode = RunMode.BACKTESTING.value
    order = pd.DataFrame()
    deal = pd.DataFrame()
    position = pd.DataFrame()
    account = pd.DataFrame()

    @classmethod
    def refresh(cls):
        cls.account = pd.DataFrame()
        cls.position = pd.DataFrame()
        cls.order = pd.DataFrame()
        cls.deal = pd.DataFrame()
