# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/5/4
# @Author  : gao
# @File    : rabbitmq_receiver_test.py
# @Project : AmazingQuant
# ------------------------------
import time

import pika

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
# channel.queue_declare(queue='hello-1')
channel.exchange_declare(exchange='direct1-logs',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True, queue='')
queue_name = result.method.queue
print(queue_name)
channel.queue_bind(exchange='direct-logs',
                   queue=queue_name,
                   routing_key='hello-1')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    print(" [x] %r:%r" % (method.routing_key, body))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(queue_name, callback, consumer_tag="hello-consumer")
# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
