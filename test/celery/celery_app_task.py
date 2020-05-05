# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : celery_app_task.py
# @Project : AmazingQuant
# ------------------------------
from celery import Celery

# broker = 'redis://127.0.0.1:6379/7'
broker = 'amqp://guest:guest@127.0.0.1:5672/'
backend = 'redis://127.0.0.1:6379/1'

cel = Celery('tasks', broker=broker, backend=backend)


@cel.task
def add(x, y):
    return x + y