# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : add_task.py
# @Project : AmazingQuant
# ------------------------------
from test.celery.celery_app_task import add
result = add.delay(1, 1)
print(result.id)
