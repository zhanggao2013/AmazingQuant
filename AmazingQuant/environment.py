# -*- coding: utf-8 -*-

__author__ = "gao"

class Environment(object):
    account = {}
    position = {}
    order = {}
    deal = {}

    @classmethod
    def refresh(cls):
        cls.account = {}
        cls.position = {}
        cls.order = {}
        cls.deal = {}