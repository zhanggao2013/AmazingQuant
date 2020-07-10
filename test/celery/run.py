# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/7/10
# @Author  : zhangdg
# @File    : run.py
# @Project : AmazingQuant
# ------------------------------

from celery import Celery
# celery worker -A celery -l info -n 1  -P eventlet
# celery flower --broker=redis://10.237.120.238:6379/13

app = Celery('celery', include=['celery.tasks'])
app.config_from_object('celery.celeryconfig')


if __name__ == '__main__':
    app.start()
    # app.worker_main()
