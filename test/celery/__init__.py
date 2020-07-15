# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : __init__.py.py
# @Project : AmazingQuant 
# ------------------------------
from celery import Celery

app = Celery('celery', include=['celery.tasks'])
app.config_from_object('celery.celeryconfig')

# celery worker -A calculation_service -l info -n 1  -P eventlet
# celeryconfig 单节点redis
# celery flower --broker=redis://10.237.102.212:6379/13
# celeryconfig redis 集群
# celery flower -A calculation_service
