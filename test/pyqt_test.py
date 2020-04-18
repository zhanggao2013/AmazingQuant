# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/25
# @Author  : gao
# @File    : pyqt_test.py
# @Project : AmazingQuant
# ------------------------------
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("打开网页例子")
        # 相当于初始化这个加载web的控件
        self.browser = QWebEngineView()
        # 加载外部页面，调用
        self.browser.load(QUrl("https://www.baidu.com"))

        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # import pyqtgraph.examples
    #
    # pyqtgraph.examples.run()
