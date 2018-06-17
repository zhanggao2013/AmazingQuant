# -*- coding: utf-8 -*-

__author__ = "gao"


class Environment(object):
    order = {}
    deal = {}
    position = {}
    account = {}

    @classmethod
    def refresh(cls):
        cls.account = {}
        cls.position = {}
        cls.order = {}
        cls.deal = {}
