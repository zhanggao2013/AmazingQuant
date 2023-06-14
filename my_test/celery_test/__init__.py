# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : __init__.py.py
# @Project : AmazingQuant 
# ------------------------------
from celery import Celery

app = Celery('celery_test', include=['celery_test.celery_app_task'])
app.config_from_object('celery_test.celeryconfig')

# celery worker -A celery_test -l info -n 1  -P eventlet
# celeryconfig 单节点redis
# celery flower --broker=redis://10.237.102.212:6379/13
# celeryconfig redis 集群
# celery flower -A celery_test -port=5555

