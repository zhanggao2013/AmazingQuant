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