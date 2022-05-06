"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: MainWindow.py
...@author: Karbob
...@date: 2020-11-04
"""
import os
import pickle
from Qt.Player import Player
from Qt.Tetris import Tetris
from Qt.Base import Button, Label
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QMouseEvent


class MainWindow(QWidget):

    screen_width: int           # 窗口的宽度
    screen_height: int          # 窗口的高度
    pixmap: QPixmap             # 临时存储图片路径
    background: Label           # 开始时的背景图片
    timer: QTimer               # 定时器
    is_mouse_press: bool        # 鼠标是否按下
    mouse_point: QPoint         # 鼠标相对窗口的位置

    # 按钮
    btn_close: Button            # 关闭窗口按钮
    btn_minimize: Button         # 最小化窗口按钮
    btn_start: Button            # 开始游戏按钮
    btn_mute: Button             # 静音按钮
    btn_cancel_mute: Button      # 取消静音按钮
    btn_next_music: Button       # 下一首音乐按钮
    btn_previous_music: Button   # 上一首音乐按钮

    button_size = 30 + 5

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)

        self.game = self.load_archive_data()
        self.player = Player(self)

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
        self.background = Label(self)
        self.pixmap = QPixmap("./icons/background.png")
        self.background.setPixmap(self.pixmap)

    def init_button(self) -> None:
        """初始化按钮属性,创建按钮"""
        # 读取qss文件
        with open("./QSS/mainWindow.qss", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
            fp.close()

        # 右上角的关闭按钮
        self.btn_close = Button(self)
        self.btn_close.setObjectName("closeButton")
        self.btn_close.setShortcut("ESC")                                     # 按钮热键esc
        self.btn_close.setToolTip("关闭")                                      # 悬停在按钮上的提示->关闭
        self.btn_close.move(self.screen_width - self.button_size, 5)          # 按钮的位置
        self.btn_close.clicked.connect(self.slot_clicked_close)

        # 右上角的最小化按钮
        self.btn_minimize = Button(self)
        self.btn_minimize.setObjectName("minimizeButton")
        self.btn_minimize.setToolTip("最小化")                                   # 悬停在按钮上的提示->最小化
        self.btn_minimize.move(self.screen_width - 2 * self.button_size, 5)     # 按钮的位置
        self.btn_minimize.clicked.connect(self.showMinimized)

        # 开始游戏的按钮
        self.btn_start = Button(self)
        self.btn_start.setObjectName("startButton")
        self.btn_start.move(self.screen_width // 2 - 100, self.screen_height // 2 - 50)     # 按钮的位置
        self.btn_start.clicked.connect(self.slot_clicked_start)

        # 静音按钮
        self.btn_mute = Button(self)
        self.btn_mute.setObjectName("muteButton")
        self.btn_mute.move(self.screen_width - 3 * self.button_size, 5)             # 按钮的位置
        self.btn_mute.hide()  # 默认隐藏
        self.btn_mute.clicked.connect(self.slot_clicked_mute)

        # 取消静音按钮
        self.btn_cancel_mute = Button(self)
        self.btn_cancel_mute.setObjectName("cancelMuteButton")
        self.btn_cancel_mute.move(self.screen_width - 3 * self.button_size, 5)     # 按钮的位置
        self.btn_cancel_mute.clicked.connect(self.slot_clicked_cancel_mute)

        # 下一首音乐按钮
        self.btn_next_music = Button(self)
        self.btn_next_music.setObjectName("nextMusicButton")
        self.btn_next_music.setToolTip("下一首")        # 悬停在按钮上的提示->下一首
        self.btn_next_music.move(self.screen_width - 4 * self.button_size, 5)       # 按钮的位置
        self.btn_next_music.clicked.connect(self.player.next_music)

        # 上一首音乐按钮
        self.btn_previous_music = Button(self)
        self.btn_previous_music.setObjectName("previousMusicButton")
        self.btn_previous_music.setToolTip("上一首")        # 悬停在按钮上的提示->上一首
        self.btn_previous_music.move(self.screen_width - 5 * self.button_size, 5)    # 按钮的位置
        self.btn_previous_music.clicked.connect(self.player.previous_music)

        # 重新开始游戏按钮
        self.game.btn_restart.clicked.connect(self.slot_clicked_restart)

    def slot_clicked_start(self) -> None:
        """点击开始游戏按钮的信号槽"""
        self.btn_start.hide()
        self.background.hide()
        self.game.start()

    def slot_clicked_restart(self) -> None:
        """点击重新开始游戏按钮的信号槽"""
        self.game.is_game_start = False
        self.game.btn_pause.hide()
        self.game.init_data()
        self.game.btn_restart.hide()
        self.game.game_over_image.hide()
        self.btn_start.show()
        self.background.show()

    def slot_clicked_mute(self) -> None:
        """点击静音按钮的信号槽"""
        self.player.cancel_mute()
        self.btn_cancel_mute.show()
        self.btn_mute.hide()

    def slot_clicked_cancel_mute(self) -> None:
        """点击取消静音按钮的信号槽"""
        self.player.mute()
        self.btn_cancel_mute.hide()
        self.btn_mute.show()

    def slot_clicked_close(self) -> None:
        """点击关闭窗口按钮"""
        if self.game.is_game_start and not self.game.is_game_over:
            # 先暂停游戏
            self.game.slot_clicked_pause()
            self.game.is_game_start = False
            # 存档
            self.save_archive_data()
        self.close()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """鼠标按下事件"""
        self.is_mouse_press = True
        self.mouse_point = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """鼠标移动事件"""
        if self.is_mouse_press:
            # 相当于原来的位置 + (鼠标移动位置 - 鼠标按下位置)
            self.move(event.globalPos() - self.mouse_point)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """鼠标释放事件"""
        self.is_mouse_press = False

    def save_archive_data(self) -> None:
        """保存存档"""
        data = {
            "is_game_start": self.game.is_game_start,
            "is_pause": self.game.is_pause,
            "block_list": self.game.block_list,
            "current_row": self.game.current_row,
            "current_column": self.game.current_column,
            "current_block_dict": self.game.current_block_dict,
            "next_block_dict": self.game.next_block_dict,
            "score": self.game.score,
        }
        with open("data.pkl", "wb") as fp:
            pickle.dump(data, fp)
            fp.close()

    def load_archive_data(self) -> Tetris:
        """读取存档"""
        game = Tetris(self)
        try:
            # 读取数据
            with open("data.pkl", "rb") as fp:
                data = pickle.load(fp)
                fp.close()
            # 恢复数据
            game.is_game_start = data["is_game_start"]
            game.is_pause = data["is_pause"]
            game.block_list = data["block_list"]
            game.current_row = data["current_row"]
            game.current_column = data["current_column"]
            game.current_block_dict = data["current_block_dict"]
            game.next_block_dict = data["next_block_dict"]
            game.score = data["score"]
            # 删除文件
            os.remove("data.pkl")
        except Exception:
            pass
        return game
