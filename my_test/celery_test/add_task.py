# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : add_task.py
# @Project : AmazingQuant
# ------------------------------
import time

from celery_test.celery_app_task import add
from celery import group

data = [1, 2, 3]*10
r1 = group([add.s(i, i + 2) for i in data]).apply_async()

for async1 in r1:
    while True:
        if async1.successful():
            result = async1.get()
            print(result)
            print('执行完成', time.time())
            # async1.forget() # 将结果删除
            break
        elif async1.failed():
            print('执行失败')
        elif async1.status == 'PENDING':
            print('任务等待中被执行')
        elif async1.status == 'RETRY':
            print('任务异常后正在重试')
        elif async1.status == 'STARTED':
            print('任务已经开始被执行')
