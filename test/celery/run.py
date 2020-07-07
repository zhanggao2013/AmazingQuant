# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : run.py
# @Project : AmazingQuant
# ------------------------------
# celery worker -A celery_app_task -l info -n 1 -c 10 -P eventlet
# eventlet 线程、gevent 协程 都可以，prefork 进程、

from test.celery.celery_app_task import cel
if __name__ == '__main__':
    cel.worker_main()
    # cel.worker_main(argv=['--loglevel=info')