# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : result.py
# @Project : AmazingQuant
# ------------------------------

from celery.result import AsyncResult
from test.celery.celery_app_task import cel

from test.celery.celery_app_task import add
result = add.delay(1, 1)
print(result.id)
a = 3
async1 = AsyncResult(id=result.id, app=cel)
while True:
    if async1.successful():
        result = async1.get()
        print(result)
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