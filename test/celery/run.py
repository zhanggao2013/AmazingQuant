# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/5
# @Author  : gao
# @File    : run.py
# @Project : AmazingQuant
# ------------------------------

from test.celery.celery_app_task import cel
if __name__ == '__main__':
    cel.worker_main()
    # cel.worker_main(argv=['--loglevel=info')