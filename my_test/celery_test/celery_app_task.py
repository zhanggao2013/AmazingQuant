# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : celery_app_task.py
# @Project : AmazingQuant
# ------------------------------
import time
import sys
# print(sys.path)
from celery_test import app
# from celery_test import app


@app.task(name='celery_test.celery_app_task.taskA')
def add(x, y):
    time.sleep(4)
    return x + y
