from kombu import Exchange, Queue

BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672/'  # 使用amqp作为消息代理
# BROKER_URL = 'redis://127.0.0.1:6378/7'  # 使用redis作为消息代理

RESULT_BROKER_TRANSPORT_OPTIONS = {"master_name": "mymaster"}

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6378/1'  # 把任务结果存在了Redis

# redis集群哨兵模式---------------
# CELERY_RESULT_BACKEND = 'sentinel://10.237.102.210:26379/14;' \
#                         'sentinel://10.237.102.211:26379/14;' \
#                         'sentinel://10.237.102.212:26379/14'
# BROKER_URL = 'sentinel://10.237.102.210:26379/13;' \
#              'sentinel://10.237.102.211:26379/13;' \
#              'sentinel://10.237.102.212:26379/13'
#
# BROKER_TRANSPORT_OPTIONS = {
#     'master_name': 'mymaster',
#     'service_name': 'mymaster',
#     'socket_timeout': 6000,
#     'visibility_timeout': 3600,
# }
# CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS
#  redis集群哨兵模式---------------


IMPORTS = ("celery.tasks",)
task_name_list = ['task_A', 'task_B', 'task_C', 'task_D']

CELERY_QUEUES = (
    Queue("for_task_A", Exchange("for_task_A"), routing_key="for_task_A"),
    Queue("for_task_B", Exchange("for_task_B"), routing_key="for_task_B"),
    Queue("for_task_C", Exchange("for_task_C"), routing_key="for_task_C"),
    Queue("for_task_D", Exchange("for_task_D"), routing_key="for_task_D")
)

CELERY_ROUTES = (
    {
        "proj_celery.tasks.taskA":
            {
                'queue': "for_task_A",
                "routing_key": "for_task_A"
            },
    },

    {
        "proj_celery.tasks.taskB":
            {
                'queue': "for_task_B",
                "routing_key": "for_task_B"
            },
    },

    {
        "proj_celery.tasks.taskC":
            {
                'queue': "for_task_C",
                "routing_key": "for_task_C"
            },
    },
    {
        "proj_celery.tasks.taskD":
            {
                'queue': "for_task_D",
                "routing_key": "for_task_D"
            },
    },
)

CELERY_TASK_SERIALIZER = 'msgpack'  # 任务序列化和反序列化使用msgpack方案
# CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 3  # 任务过期时间

CELERY_ACCEPT_CONTENT = ['json', 'msgpack']  # 指定接受的内容类型

CELERY_REJECT_ON_WORKER_LOST = True  # 当worker进程意外退出时，task会被放回到队列中
CELERY_ACKS_LATE = True  # 只有当worker完成了这个task时，任务才被标记为ack状态
