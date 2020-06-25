# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : celery_app_task.py
# @Project : AmazingQuant
# ------------------------------
from celery import Celery
import time
# broker = 'redis://127.0.0.1:6378/7'
broker = 'amqp://guest:guest@127.0.0.1:5672/'
backend = 'redis://127.0.0.1:6378/1'

cel = Celery('tasks', broker=broker, backend=backend)


a = 1
a += 1


@cel.task(name='celery_app_task.task')
def add(x, y):
    time.sleep(4)
    return x + y + a
