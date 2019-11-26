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
        self.browser.load(QUrl("file:///F:/%E5%B7%A5%E4%BD%9C/%E6%8A%95%E5%90%8E%E5%88%86%E6%9E%90svn/account_analysis/%E4%B8%8A%E6%B6%A8%E4%B8%8B%E8%B7%8C%E5%8C%BA%E9%97%B4.html"))

        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # import pyqtgraph.examples
    #
    # pyqtgraph.examples.run()
