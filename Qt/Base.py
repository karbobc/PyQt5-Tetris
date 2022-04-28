"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: Base.py
...@author: Karbob
...@date: 2022-04-28
"""
from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)


class Button(QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super(Button, self).__init__(*args, **kwargs)
        # 0边距
        self.setContentsMargins(0, 0, 0, 0)
        # 点击按钮之后马上清除焦点
        self.clicked.connect(self.clearFocus)


class Label(QLabel):

    def __init__(self, *args, **kwargs) -> None:
        super(Label, self).__init__(*args, **kwargs)
        # 0边距
        self.setContentsMargins(0, 0, 0, 0)


class HLinearLayout(QHBoxLayout):

    def __init__(self, *args, **kwargs) -> None:
        super(HLinearLayout, self).__init__(*args, **kwargs)
        # 0边距
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)


class VLinearLayout(QVBoxLayout):

    def __init__(self, *args, **kwargs) -> None:
        super(VLinearLayout, self).__init__(*args, **kwargs)
        # 0边距
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
