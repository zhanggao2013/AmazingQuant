# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : result.py
# @Project : AmazingQuant
# ------------------------------

from celery.result import AsyncResult
from test.celery.celery_app_task import cel
async1 = AsyncResult(id="303ffc7d-a71a-4052-81b2-8a9e38c9d750", app=cel)

if async1.successful():
    result = async1.get()
    print(result)
    async1.forget() # 将结果删除
elif async1.failed():
    print('执行失败')
elif async1.status == 'PENDING':
    print('任务等待中被执行')
elif async1.status == 'RETRY':
    print('任务异常后正在重试')
elif async1.status == 'STARTED':
    print('任务已经开始被执行')