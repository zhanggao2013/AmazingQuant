# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : add_task.py
# @Project : AmazingQuant
# ------------------------------
from .celery_app_task import add
from celery import group

data = [1, 2, 3]
r1 = group([add.s(i, i + 2) for i in data]).apply_async()
