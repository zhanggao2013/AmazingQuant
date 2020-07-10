# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : celery_app_task.py
# @Project : AmazingQuant
# ------------------------------
import time
from test.celery import app


@app.task(name='celery_app_task.task')
def add(x, y):
    time.sleep(4)
    return x + y
