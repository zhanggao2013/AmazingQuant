# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/1/20
# @Author  : gao
# @File    : logger.py
# @Project : AmazingQuant 
# ------------------------------
import logging
import logging.handlers
import os
import time


class Logger(object):
    def __init__(self, logger_dir, set_level="DEBUG"):
        self.logger = logging.getLogger(logger_dir)
        # 设置输出的等级
        level_dict = {'NOSET': logging.NOTSET,
                      'DEBUG': logging.DEBUG,
                      'INFO': logging.INFO,
                      'WARNING': logging.WARNING,
                      'ERROR': logging.ERROR,
                      'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        if os.path.exists(logger_dir):
            pass
        else:
            os.mkdir(logger_dir)

        logging.basicConfig(level=level_dict[set_level],
                            format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=logger_dir + '/' + logger_dir + '.log',
                            filemode='a')
        file_handler = logging.FileHandler(filename=logger_dir + '/' + logger_dir + '.log', encoding="utf-8")

        # 控制台句柄
        console = logging.StreamHandler()
        # 添加内容到日志句柄中
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)
        self.logger.removeHandler(file_handler)

    def info(self, *message):
        self.logger.info(message)

    def debug(self, *message):
        self.logger.debug(message)

    def warning(self, *message):
        self.logger.warning(message)

    def error(self, *message):
        self.logger.error(message)


if __name__ == '__main__':
    logger = Logger("test")
    logger.info("this is info", 'qwe')
    logger.debug("this is debug")
    logger.error("this is error")
    logger.warning("this is warning")
