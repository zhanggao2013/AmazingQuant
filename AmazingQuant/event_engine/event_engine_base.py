# -*- coding: utf8 -*-

_author_ = "gao"

from queue import Queue, Empty
from threading import Thread
from time import sleep
from collections import defaultdict


class EventEngineBase(object):
    """
    变量说明
    _queue：私有变量，事件队列
    _active：私有变量，事件引擎开关
    _thread：私有变量，事件处理线程
    _timer：私有变量，计时器
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

        # 计时器，用于触发计时器事件
        self._timer = Thread(target=self._runTimer)
        self._timer_active = False  # 计时器工作状态
        self._timer_sleep = 1  # 计时器触发间隔（默认1秒）

        # 这里的_handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self._handlers = defaultdict(list)

        # _general_handlers是一个列表，用来保存通用回调函数（所有事件均调用）
        self._general_handlers = []

    def _run(self):
        """引擎运行"""
        while self._active == True:
            try:
                event = self._queue.get(block=True, timeout=1)  # 获取事件的阻塞时间设为1秒
                self._process(event)
            except Empty:
                pass

    def _process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self._handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self._handlers[event.type_]]

        # 调用通用处理函数进行处理
        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    def _runTimer(self):
        """运行在计时器线程中的循环函数"""
        while self._timer_active:
            # 创建计时器事件
            event = Event(type_=EVENT_TIMER)

            # 向队列中存入计时器事件
            self.put(event)

            # 等待
            sleep(self._timer_sleep)

    def start(self, timer=True):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self._active = True

        # 启动事件处理线程
        self._thread.start()

        # 启动计时器，计时器事件间隔默认设定为1秒
        if timer:
            self._timer_active = True
            self._timer.start()

    def stop(self):
        """停止引擎"""
        # 将引擎设为停止
        self._active = False

        # 停止计时器
        self._timer_active = False
        self._timer.join()

        # 等待事件处理线程退出
        self._thread.join()

    def register(self, type_, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handlerList = self._handlers[type_]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)

    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handlerList = self._handlers[type_]

        # 如果该函数存在于列表中，则移除
        if handler in handlerList:
            handlerList.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handlerList:
            del self._handlers[type_]

    def put(self, event):
        """向事件队列中存入事件"""
        self._queue.put(event)

    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)


class Event(object):
    """事件对象"""

    def __init__(self, type_=None):
        """Constructor"""
        self.type_ = type_  # 事件类型
        self.dict_ = {}  # 字典用于保存具体的事件数据


def test():
    """测试函数"""
    import sys
    from datetime import datetime
    from qtpy.QtCore import QCoreApplication

    def simpletest(event):
        print(u'处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

    app = QCoreApplication(sys.argv)

    ee = EventEngine2()
    # ee.register(EVENT_TIMER, simpletest)
    ee.registerGeneralHandler(simpletest)
    ee.start()

    app.exec_()
