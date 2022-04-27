"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: MainWindow.py
...@author: Karbob
...@date: 2020-11-04
"""
from Qt.Player import Player
from Qt.Tetris import Tetris
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon


class MainWindow(QWidget):

    screen_width: int           # 窗口的宽度
    screen_height: int          # 窗口的高度
    pixmap: QPixmap             # 临时存储图片路径
    background: QLabel          # 开始时的背景图片
    timer: QTimer               # 定时器

    # 按钮
    btn_close: QPushButton            # 关闭窗口按钮
    btn_minimize: QPushButton         # 最小化窗口按钮
    btn_start: QPushButton            # 开始游戏按钮
    btn_mute: QPushButton             # 静音按钮
    btn_cancel_mute: QPushButton      # 取消静音按钮
    btn_next_music: QPushButton       # 下一首音乐按钮
    btn_previous_music: QPushButton   # 上一首音乐按钮

    button_size = 30 + 5

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.player = Player(self)
        self.game = Tetris(self)

        self.screen_width = 900
        self.screen_height = 800
        self.init_window()
        self.init_ui()
        self.init_button()

    def init_window(self) -> None:
        """初始化窗口"""
        self.resize(self.screen_width, self.screen_height)    # 窗口大小
        self.setWindowTitle("Tetris")
        self.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.setWindowState(Qt.WindowActive)        # 活动窗口
        self.setWindowIcon(QIcon("./icons/captain_America.ico"))    # 设置图标

    def init_ui(self) -> None:
        """绘制背景图片"""
        # 第一张背景图片
        self.background = QLabel(self)
        self.pixmap = QPixmap("./icons/background.png")
        self.background.setPixmap(self.pixmap)

    def init_button(self) -> None:
        """初始化按钮属性,创建按钮"""
        # 读取qss文件
        with open("./QSS/mainWindow.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
            fp.close()

        # 右上角的关闭按钮
        self.btn_close = QPushButton(self)
        self.btn_close.setObjectName("closeButton")
        self.btn_close.setShortcut("ESC")      # 按钮热键esc
        self.btn_close.setToolTip("关闭")        # 悬停在按钮上的提示->关闭
        self.btn_close.move(self.screen_width - self.button_size, 5)          # 按钮的位置
        self.btn_close.clicked.connect(self.close)

        # 右上角的最小化按钮
        self.btn_minimize = QPushButton(self)
        self.btn_minimize.setObjectName("minimizeButton")
        self.btn_minimize.setToolTip("最小化")        # 悬停在按钮上的提示->最小化
        self.btn_minimize.move(self.screen_width - 2 * self.button_size, 5)     # 按钮的位置
        self.btn_minimize.clicked.connect(self.showMinimized)

        # 开始游戏的按钮
        self.btn_start = QPushButton(self)
        self.btn_start.setObjectName("startButton")
        self.btn_start.move(self.screen_width // 2 - 100, self.screen_height // 2 - 50)     # 按钮的位置
        self.btn_start.clicked.connect(self.slot_clicked_start)

        # 静音按钮
        self.btn_mute = QPushButton(self)
        self.btn_mute.setObjectName("muteButton")
        self.btn_mute.move(self.screen_width - 3 * self.button_size, 5)   # 按钮的位置
        self.btn_mute.hide()  # 默认隐藏
        self.btn_mute.clicked.connect(self.slot_clicked_mute)

        # 取消静音按钮
        self.btn_cancel_mute = QPushButton(self)
        self.btn_cancel_mute.setObjectName("cancelMuteButton")
        self.btn_cancel_mute.move(self.screen_width - 3 * self.button_size, 5)     # 按钮的位置
        self.btn_cancel_mute.clicked.connect(self.slot_clicked_cancel_mute)

        # 下一首音乐按钮
        self.btn_next_music = QPushButton(self)
        self.btn_next_music.setObjectName("nextMusicButton")
        self.btn_next_music.setToolTip("下一首")        # 悬停在按钮上的提示->下一首
        self.btn_next_music.move(self.screen_width - 4 * self.button_size, 5)  # 按钮的位置
        self.btn_next_music.clicked.connect(self.player.nextMusic)

        # 上一首音乐按钮
        self.btn_previous_music = QPushButton(self)
        self.btn_previous_music.setObjectName("previousMusicButton")
        self.btn_previous_music.setToolTip("上一首")        # 悬停在按钮上的提示->上一首
        self.btn_previous_music.move(self.screen_width - 5 * self.button_size, 5)    # 按钮的位置
        self.btn_previous_music.clicked.connect(self.player.previousMusic)

    def set_timer(self) -> None:
        """设置Timer, 每隔500ms检测游戏是否结束"""
        self.timer = QTimer()
        interval = 500
        self.timer.start(interval)
        self.timer.timeout.connect(self.game_over)

    def game_over(self) -> None:
        """判断游戏是否结束"""
        if self.game.isGameOver is True:
            self.background.show()
            self.btn_start.show()
            self.timer.disconnect()
            self.game.isGameStart = False
            self.game.restartButton.hide()
            self.game.gameOverImage.hide()

    def slot_clicked_start(self) -> None:
        """点击开始游戏按钮的信号槽"""
        self.btn_start.hide()
        self.background.hide()
        self.game.start()
        self.set_timer()

    def slot_clicked_mute(self) -> None:
        """点击静音按钮的信号槽"""
        self.player.cancelMute()
        self.btn_cancel_mute.show()
        self.btn_mute.hide()

    def slot_clicked_cancel_mute(self) -> None:
        """点击取消静音按钮的信号槽"""
        self.player.mute()
        self.btn_cancel_mute.hide()
        self.btn_mute.show()
