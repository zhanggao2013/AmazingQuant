# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_engine_base.py.py
# @Project : AmazingQuant
# ------------------------------
from queue import Queue, Empty
from threading import Thread, RLock
from time import sleep
from collections import defaultdict

from AmazingQuant.constant import EventType


class EventEngineBase(object):
    """
    变量说明
    _queue：私有变量，事件队列
    _active：私有变量，事件引擎开关
    _thread：私有变量，事件处理线程
    _handlers：私有变量，事件处理函数字典


    方法说明
    _run: 私有方法，事件处理线程连续运行用
    _process: 私有方法，处理事件，调用注册在引擎中的监听函数
    start: 公共方法，启动引擎
    stop：公共方法，停止引擎
    register：公共方法，向引擎中注册监听函数
    unregister：公共方法，向引擎中注销监听函数
    put：公共方法，向事件队列中存入新的事件
    """

    def __init__(self):
        # 事件队列
        self._queue = Queue()

        # 事件引擎开关
        self._active = False

        # 事件处理线程
        self._thread = Thread(target=self._run)

        # 线程锁
        self._lock = RLock()

        # 这里的_handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self._handlers = defaultdict(list)

    def _run(self):
        """引擎运行"""
        while self._active:
            sleep(0.00000000000000000000001)
            try:
                event = self._queue.get(block=False, timeout=0)  # 获取事件设为非阻塞
                self._lock.acquire()
                self._process(event)
                self._lock.release()
            except Empty:
                break

    def _process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.event_type in self._handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self._handlers[event.event_type]]

    def start(self):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self._active = True

        # 启动事件处理线程
        self._thread.start()

    def stop(self):
        """停止引擎"""

        # 队列为空的时候，将引擎设为False
        while True:
            sleep(0.00000000000000000000000001)
            if self._queue.empty():
                self._active = False
                break

        # 等待事件处理线程退出
        self._thread.join()

    def register(self, event_type, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handler_list = self._handlers[event_type]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, event_type, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handler_list = self._handlers[event_type]

        # 如果该函数存在于列表中，则移除
        if handler in handler_list:
            handler_list.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handler_list:
            del self._handlers[event_type]

    def put(self, event):
        """向事件队列中存入事件"""
        self._queue.put(event)


class Event(object):
    """事件对象"""

    def __init__(self, event_type=None):
        """Constructor"""
        self.event_type = event_type  # 事件类型
        self.event_data_dict = {}  # 字典用于保存具体的事件数据


class TestOne(object):
    def test(self):
        """测试函数"""
        from datetime import datetime

        def simpletest(event):
            print(u'处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

        ee = EventEngineBase()
        ee.put(Event(EventType.EVENT_MARKET.value))
        # ee.register(EventType.EVENT_TIMER.value, simpletest)
        ee.register(EventType.EVENT_MARKET.value, simpletest)
        # ee.registerGeneralHandler(simpletest)
        ee.start()
        ee.stop()


if __name__ == "__main__":
    aa = TestOne()
    aa.test()
