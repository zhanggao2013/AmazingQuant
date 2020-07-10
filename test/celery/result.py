# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : result.py
# @Project : AmazingQuant
# ------------------------------
import time
from celery.result import AsyncResult
from test.celery.run import app

from test.celery.celery_app_task import add
result = add.delay(1, 1)
print(result.id)
a = 3
async1 = AsyncResult(id=result.id, app=app)

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