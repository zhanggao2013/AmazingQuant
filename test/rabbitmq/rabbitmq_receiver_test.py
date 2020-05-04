# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/4
# @Author  : gao
# @File    : rabbitmq_receiver_test.py
# @Project : AmazingQuant
# ------------------------------


import pika

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


# 告诉rabbitmq使用callback来接收信息
# channel.basic_consume(callback, queue='hello', no_ack=True)
channel.basic_consume("hello", callback, consumer_tag="hello-consumer")
# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
