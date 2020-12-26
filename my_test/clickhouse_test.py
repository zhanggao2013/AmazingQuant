# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/12/26
# @Author  : gao
# @File    : clickhouse_test.py
# @Project : AmazingQuant
# ------------------------------
from clickhouse_driver import Client as click_client


def click_server(host: str, user: str, password: str, port='8123', database='', query=''):
    """
    查询clickhouse数据
    :param host: clickhouse host
    :param user: 账号
    :param password: 密码
    :param port: 端口
    :param database: 查询库
    :param query: 查询语句
    :return: list
    """
    chs_host = host
    chs_user = user
    chs_pwd = password
    chs_port = port
    chs_database = database
    client = click_client(host=chs_host, user=chs_user, password=chs_pwd, database=chs_database)
    ans = client.execute(query)
    return ans


# create_test = click_server(host='localhost', user='default', password='123456', database='AmazingQuant',
#                           query="CREATE TABLE test01( id UInt16,col1 String,col2 String,create_date date ) ENGINE = MergeTree(create_date, (id), 8123)")

insert_test = click_server(host='localhost', user='default', password='123456', database='AmazingQuant',
                          query="insert into test01(id, col1) values (1, 'first')")

