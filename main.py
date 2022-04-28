"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: main.py
...@author: Karbob
...@date: 2020-11-04
"""
import sys
from Qt.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
