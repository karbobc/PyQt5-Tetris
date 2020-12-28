"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: main.py
...@author: Karbob
...@date: 2020-11-04
"""

# todo
# 按钮的事件和按键的事件冲突

import sys
from Qt.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
