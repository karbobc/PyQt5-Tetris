"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: MainWindow.py
...@author: Karbob
...@date: 2020-11-04
"""

import sys
from .Player import Player
from .Tetris import Tetris
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon

class MainWindow(QWidget):

    screenWidth = None      # 窗口的宽度
    screenHeight = None     # 窗口的高度
    pixmap = None           # 临时存储图片路径
    background = None       # 开始时的背景图片
    timer = None            # 定时器

    # 按钮
    closeButton = None          # 关闭窗口按钮
    minimizeButton = None       # 最小化窗口按钮
    startButton = None          # 开始游戏按钮
    muteButton = None           # 静音按钮
    cancelMuteButton = None     # 取消静音按钮
    nextMusicButton = None      # 下一首音乐按钮
    previousMusicButton = None  # 上一首音乐按钮

    buttonSize = 30 + 5

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # self.parent = parent

        self.player = Player(self)
        self.game = Tetris(self)

        self.screenWidth = 900
        self.screenHeight = 800
        self.initWindow()
        self.initUI()
        self.initButton()


    def initWindow(self):
        """初始化窗口"""
        self.resize(self.screenWidth, self.screenHeight)    # 窗口大小
        self.setWindowTitle('Tetris')
        self.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.setWindowState(Qt.WindowActive)        # 活动窗口
        self.setWindowIcon(QIcon('./icons/captain_America.ico'))    # 设置图标

    def initUI(self):
        """绘制背景图片"""
        # 第一张背景图片
        self.background = QLabel(self)
        self.pixmap = QPixmap('./icons/background.png')
        self.background.setPixmap(self.pixmap)

    def initButton(self):
        """初始化按钮属性,创建按钮"""
        # 读取qss文件
        with open('./QSS/mainWindow.qss', 'r', encoding='utf-8') as fp:
            self.setStyleSheet(fp.read())
            fp.close()

        # 右上角的关闭按钮
        self.closeButton = QPushButton(self)
        self.closeButton.setObjectName('closeButton')
        self.closeButton.setShortcut('ESC')      # 按钮热键esc
        self.closeButton.setToolTip('关闭')        # 悬停在按钮上的提示->关闭
        self.closeButton.move(self.screenWidth - self.buttonSize, 5)          # 按钮的位置
        self.closeButton.clicked.connect(self.close)

        # 右上角的最小化按钮
        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setObjectName('minimizeButton')
        self.minimizeButton.setToolTip('最小化')        # 悬停在按钮上的提示->最小化
        self.minimizeButton.move(self.screenWidth - 2*self.buttonSize, 5)     # 按钮的位置
        self.minimizeButton.clicked.connect(self.showMinimized)

        # 开始游戏的按钮
        self.startButton = QPushButton(self)
        self.startButton.setObjectName('startButton')
        self.startButton.move(self.screenWidth // 2 - 100, self.screenHeight // 2 - 50)     # 按钮的位置
        self.startButton.clicked.connect(lambda: {
            self.startButton.hide(),
            self.background.hide(),
            self.game.start(),
            self.setTimer(),
        })

        # 静音按钮
        self.muteButton = QPushButton(self)
        self.muteButton.setObjectName('muteButton')
        self.muteButton.move(self.screenWidth - 3*self.buttonSize, 5)   # 按钮的位置
        self.muteButton.hide()  # 默认隐藏
        self.muteButton.clicked.connect(lambda: {
            self.player.cancelMute(),
            self.cancelMuteButton.show(),
            self.muteButton.hide(),
        })

        # 取消静音按钮
        self.cancelMuteButton = QPushButton(self)
        self.cancelMuteButton.setObjectName('cancelMuteButton')
        self.cancelMuteButton.move(self.screenWidth - 3*self.buttonSize, 5)     # 按钮的位置
        self.cancelMuteButton.clicked.connect(lambda: {
            self.player.mute(),
            self.cancelMuteButton.hide(),
            self.muteButton.show(),
        })

        # 下一首音乐按钮
        self.nextMusicButton = QPushButton(self)
        self.nextMusicButton.setObjectName('nextMusicButton')
        self.nextMusicButton.setToolTip('下一首')        # 悬停在按钮上的提示->下一首
        self.nextMusicButton.move(self.screenWidth - 4*self.buttonSize, 5)  # 按钮的位置
        self.nextMusicButton.clicked.connect(self.player.nextMusic)

        # 上一首音乐按钮
        self.previousMusicButton = QPushButton(self)
        self.previousMusicButton.setObjectName('previousMusicButton')
        self.previousMusicButton.setToolTip('上一首')        # 悬停在按钮上的提示->上一首
        self.previousMusicButton.move(self.screenWidth - 5*self.buttonSize, 5)    # 按钮的位置
        self.previousMusicButton.clicked.connect(self.player.previousMusic)

    def setTimer(self):
        """设置Timer, 每隔500ms检测游戏是否结束"""
        self.timer = QTimer()
        interval = 500
        self.timer.start(interval)
        self.timer.timeout.connect(self.gameOver)

    def gameOver(self):
        """判断游戏是否结束"""
        if self.game.isGameOver is True:
            self.background.show()
            self.startButton.show()
            self.timer.disconnect()
            self.game.isGameStart = False
            self.game.restartButton.hide()
            self.game.gameOverImage.hide()
