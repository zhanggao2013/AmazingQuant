# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_engine_base.py.py
# @Project : AmazingQuant
# ------------------------------
import asyncio
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

    # def __init__(self):
    def __init__(self, loop):
        self._thread = loop
        # 事件队列
        self._queue = Queue()

        # 事件引擎开关
        self._active = False

        # 事件处理线程
        # self._thread = asyncio.new_event_loop()

        # 计时器，用于触发计时器事件
        self._timer = Thread(target=self._run_timer)
        self._timer_active = False  # 计时器工作状态
        self._timer_sleep = 1  # 计时器触发间隔（默认1秒）

        # 这里的_handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self._handlers = defaultdict(list)

    async def _run(self, event):
        """引擎运行"""
        while self._active:
            try:
                # event = self._queue.get(block=False, timeout=0)  # 获取事件设为非阻塞
                print("_run")
                for handler in self._handlers[event.event_type]:
                    await handler(event)
            except Empty:
                break

    def _run_timer(self):
        """运行在计时器线程中的循环函数"""
        while self._timer_active:
            # 创建计时器事件
            event = Event(event_type=EventType.EVENT_TIMER.value)

            # 等待
            sleep(self._timer_sleep)

    def start(self, event, timer=True):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self._active = True

        # 启动事件处理线程
        asyncio.run(self._run(event))

        # 启动计时器，计时器事件间隔默认设定为1秒
        if timer:
            self._timer_active = True
            self._timer.start()

    def stop(self):
        """停止引擎"""
        self._thread.stop()
        # 停止计时器
        if self._timer_active:
            self._timer_active = False
            self._timer.join()

        # 等待事件处理线程退出
        # self._thread.join()

    def register(self, event_type, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handler_list = self._handlers[event_type]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handler_list:
            handler_list.append(handler)



class Event(object):
    """事件对象"""

    def __init__(self, event_type=None):
        """Constructor"""
        self.event_type = event_type  # 事件类型
        self.event_data_dict = {}  # 字典用于保存具体的事件数据


class TestOne(object):
    def __init__(self, loop1):
        self.loop1 = loop1

    def tes(self):
        """测试函数"""
        from datetime import datetime

        async def simpletest_1(event):
            print(u'simpletest_1：{}'.format(str(datetime.now())))

        ee = EventEngineBase(self.loop1)
        ee.register(EventType.EVENT_MARKET.value, simpletest_1)
        ee.start(Event(EventType.EVENT_MARKET.value))
        # ee.stop()

class TestTwo(object):
    def __init__(self, loop2):
        self.loop2 = loop2

    def tes(self):
        """测试函数"""
        from datetime import datetime

        async def simpletest_2(event):
            print(u'simpletest_2：{}'.format(str(datetime.now())))

        async def test_2(event):
            loop1 = asyncio.new_event_loop()
            aa = TestOne(loop1)
            aa.tes()

        ee = EventEngineBase(self.loop2)
        ee.register(EventType.EVENT_MARKET.value, simpletest_2)
        ee.register(EventType.EVENT_MARKET.value, test_2)
        ee.start(Event(EventType.EVENT_MARKET.value))
        ee.stop()


if __name__ == "__main__":
    loop2 = asyncio.new_event_loop()
    # aa = TestOne()
    # aa.tes()
    bb = TestTwo(loop2)
    bb.tes()

# import asyncio
#
# async def factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({i})...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#
# async def main0():
#     # Schedule three calls *concurrently*:
#     await asyncio.gather(
#         factorial("A", 2),
#     )
# async def main1():
#     # Schedule three calls *concurrently*:
#     await asyncio.gather(
#         main0(),
#         factorial("B", 3),
#         factorial("C", 4),
#     )
#
# asyncio.run(main1())
