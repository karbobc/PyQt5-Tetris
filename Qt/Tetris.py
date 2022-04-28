"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: Tetris.py
...@author: Karbob
...@date: 2020-11-04
"""

import random
from typing import Dict, Any, List
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from Qt.Base import Button, Label
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect, QTimer, QUrl
from PyQt5.QtGui import (
    QPixmap,
    QPen,
    QPainter,
    QColor,
    QFont,
    QFontDatabase,
    QPaintEvent,
    QKeyEvent,
    QKeySequence,
    QFocusEvent,
)


class Tetris(QWidget):

    screen_width: int                           # 窗口宽度
    screen_height: int                          # 窗口高度
    is_game_start: bool                         # 游戏是否开始
    is_game_over: bool                          # 游戏是否结束
    is_pause: bool                              # 游戏是否暂停
    btn_pause: Button                           # 暂停游戏按钮
    btn_resume: Button                          # 继续游戏按钮
    btn_restart: Button                         # 重新开始游戏按钮
    game_over_image: Label                      # 游戏结束时显示的图片
    block_size: int                             # 一个方块的大小(像素px)
    all_rows: int                               # 所有的行
    all_columns: int                            # 所有的列
    all_blocks: List[List[int]]                 # 二维数组, 记录方块
    current_row: int                            # 当前行
    current_column: int                         # 当前列
    drop_timer: QTimer                          # 方块下降的定时器
    update_timer: QTimer                        # 屏幕更新的定时器
    remove_block_timer: QTimer                  # 消除方块的定时器
    drop_interval: int                          # 方块下降定时器的时间间隔
    update_interval: int                        # 屏幕更新定时器的时间间隔
    remove_block_interval: int                  # 消除方块定时器的时间间隔
    blocks: Dict[str, List[List[List[int]]]]    # 枚举所有的方块
    block_dict: Dict[str, Any]                  # 存储方块属性的字典
    next_block_dict: Dict[str, Any]             # 存储下一个方块属性的字典
    block: List[List[int]]                      # 当前的方块
    shape: str                                  # 当前方块的类型
    index: int                                  # 当前方块类型的下标
    score: int                                  # 得分情况
    pixmap: QPixmap                             # 临时存储图片路径
    painter: QPainter                           # 画笔
    font: QFont                                 # 字体

    def __init__(self, *args, **kwargs) -> None:
        super(Tetris, self).__init__(*args, **kwargs)

        self.screen_width = 900
        self.screen_height = 800
        self.is_game_start = False
        self.is_game_over = True
        self.is_pause = True
        # self.setFocusPolicy(Qt.StrongFocus)         # 设置焦点, 监听键盘
        self.resize(self.screen_width, self.screen_height)

        self.init_button()
        self.init_image()

    def init_button(self) -> None:
        """初始化重新开始游戏的按钮"""
        # 暂停游戏按钮
        self.btn_pause = Button(self)
        self.btn_pause.setObjectName("pauseButton")
        self.btn_pause.setShortcut(QKeySequence(Qt.Key_P))
        self.btn_pause.setToolTip("暂停")  # 悬停在按钮上的提示->暂停
        self.btn_pause.move(self.screen_width - 210, 5)  # 按钮的位置
        self.btn_pause.hide()  # 默认隐藏
        self.btn_pause.clicked.connect(self.slot_clicked_pause)

        # 继续游戏按钮
        self.btn_resume = Button(self)
        self.btn_resume.setObjectName("resumeButton")
        self.btn_resume.setToolTip("继续")  # 悬停在按钮上的提示->继续
        self.btn_resume.move(self.screen_width - 210, 5)  # 按钮的位置
        self.btn_resume.hide()  # 默认隐藏
        self.btn_resume.clicked.connect(self.slot_clicked_resume)

        # 重新开始游戏按钮
        self.btn_restart = Button(self)
        self.btn_restart.setObjectName("restartButton")
        self.btn_restart.move(self.screen_width // 2 - 200, self.screen_height // 2 - 50)
        self.btn_restart.hide()       # 默认隐藏
        self.btn_restart.clicked.connect(self.game_over)

    def init_image(self) -> None:
        """初始化游戏结束的图片"""
        self.game_over_image = Label(self)
        self.game_over_image.setPixmap(QPixmap("./icons/game_over.png"))
        self.game_over_image.move(self.screen_width // 24, self.screen_height // 4)
        self.game_over_image.hide()   # 默认隐藏

    def init_settings(self) -> None:
        """初始化方块的一些初始值"""
        self.blocks = {
            "L Shape": [[[0, 0], [0, -1], [0, -2], [1, -2]], [[-1, -1], [0, -1], [1, -1], [-1, -2]],
                        [[-1, 0], [0, 0], [0, -1], [0, -2]], [[-1, -1], [0, -1], [1, -1], [1, 0]]],
            "J Shape": [[[0, 0], [0, -1], [0, -2], [-1, -2]], [[-1, 0], [-1, -1], [0, -1], [1, -1]],
                        [[0, 0], [1, 0], [0, -1], [0, -2]], [[-1, -1], [0, -1], [1, -1], [1, -2]]],
            "Z Shape": [[[-1, 0], [0, 0], [0, -1], [1, -1]], [[0, 0], [0, -1], [-1, -1], [-1, -2]],
                        [[-1, 0], [0, 0], [0, -1], [1, -1]], [[0, 0], [0, -1], [-1, -1], [-1, -2]]],
            "S Shape": [[[-1, 0], [-1, -1], [0, -1], [0, -2]], [[0, 0], [1, 0], [-1, -1], [0, -1]],
                        [[-1, 0], [-1, -1], [0, -1], [0, -2]], [[0, 0], [1, 0], [-1, -1], [0, -1]]],
            "O Shape": [[[-1, 0], [0, 0], [-1, -1], [0, -1]], [[-1, 0], [0, 0], [-1, -1], [0, -1]],
                        [[-1, 0], [0, 0], [-1, -1], [0, -1]], [[-1, 0], [0, 0], [-1, -1], [0, -1]]],
            "I Shape": [[[0, 0], [0, -1], [0, -2], [0, -3]], [[-2, -1], [-1, -1], [0, -1], [1, -1]],
                        [[0, 0], [0, -1], [0, -2], [0, -3]], [[-2, -1], [-1, -1], [0, -1], [1, -1]]],
            "T Shape": [[[-1, -1], [0, -1], [1, -1], [0, -2]], [[0, 0], [-1, -1], [0, -1], [0, -2]],
                        [[0, 0], [-1, -1], [0, -1], [1, -1]], [[0, 0], [0, -1], [1, -1], [0, -2]]]
        }
        self.score = 0
        self.block_size = 40     # 方块的大小
        self.all_rows = 20       # 总共20行
        self.all_columns = 15    # 总共15列
        self.current_row = self.all_rows + 4   # +4行是用来放置待出现的方块的
        self.current_column = self.all_columns // 2
        self.all_blocks = [[0 for row in range(self.all_columns)] for column in range(self.all_rows + 5)]
        self.all_blocks[0] = [1 for column in range(self.all_columns)]    # 用来判断方块是否到底
        # print(self.allBlock)

    def init_font(self) -> None:
        """初始化字体"""
        # 使用本地字体
        font_id = QFontDatabase.addApplicationFont("./Font/Consolas Italic.ttf")
        self.font = QFont()
        self.font.setFamily(QFontDatabase.applicationFontFamilies(font_id)[0])
        self.font.setItalic(True)   # 斜体
        self.font.setBold(True)     # 粗体
        self.font.setPixelSize(40)  # 字体大小

    def init_timer(self) -> None:
        """初始化定时器"""
        # 方块下降的定时器
        self.drop_timer = QTimer(self)
        self.drop_interval = 500     # 每0.5秒下降一格
        self.drop_timer.start(self.drop_interval)
        self.drop_timer.timeout.connect(self.block_drop)

        # paintEvent更新的定时器
        self.update_timer = QTimer(self)
        self.update_interval = 10
        self.update_timer.start(self.update_interval)
        self.update_timer.timeout.connect(self.update)

        # 消除方块的定时器
        self.remove_block_timer = QTimer(self)
        self.remove_block_interval = 150
        self.remove_block_timer.start(self.remove_block_interval)
        self.remove_block_timer.timeout.connect(self.remove_block)

    def slot_clicked_pause(self) -> None:
        """点击暂停按钮的信号槽"""
        self.pause()
        self.btn_pause.hide()
        self.btn_resume.show()

    def slot_clicked_resume(self) -> None:
        """点击继续游戏按钮的信号槽"""
        self.resume()
        self.btn_resume.hide()
        self.btn_pause.show()

    def get_block(self) -> Dict[str, Any]:
        """获取方块"""
        shape = random.choice(list(self.blocks.keys()))     # 选择随机方块的类型
        index = random.randint(0, 3)
        # if shape == "L Shape" and index == 3:
        #     pass
        block = self.blocks[shape][index]
        return {
            "shape": shape,
            "index": index,
            "block": block,
        }

    def get_current_block(self) -> None:
        """获取目前的方块"""
        self.block_dict = self.next_block_dict
        self.shape = self.block_dict["shape"]
        self.index = self.block_dict["index"]
        self.block = self.block_dict["block"]
        self.next_block_dict = self.get_block()

    def block_drop(self) -> None:
        """每运行一次, 方块下降一格, 通过QTimer每隔一定时间运行一次"""
        for position1 in self.block:
            x = position1[0] + self.current_column    # x->column
            y = position1[1] + self.current_row       # y->row
            # print(x, y)
            if self.all_blocks[y - 1][x] == 1:
                for position2 in self.block:
                    self.all_blocks[position2[1] + self.current_row][position2[0] + self.current_column] = 1
                break
        else:
            # 下落方块没有接触到其他方块或者没有到底, 继续下降
            self.current_row -= 1
            return

        # 判断游戏结束
        if 1 in self.all_blocks[self.all_rows]:
            self.pause()
            self.update()
            self.remove_block_timer.disconnect()
            self.update_timer.disconnect()
            self.btn_pause.hide()
            self.game_over_image.show()
            self.btn_restart.show()
            return

        # 方块下落完成, 获取下一个方块
        self.get_current_block()
        self.current_row = self.all_rows + 4
        self.current_column = self.all_columns // 2

    def remove_block(self) -> None:
        """消除方块"""
        # 叠满一行时消除方块, 从上往下消除
        for row in range(self.all_rows, 0, -1):
            if 0 not in self.all_blocks[row]:
                # 消除方块时触发音效, 消除一行触发一次
                player = QMediaPlayer(self)
                player.setMedia(QMediaContent(QUrl.fromLocalFile("./AudioFrequency/dingdong.mp3")))
                player.play()

                self.all_blocks.pop(row)  # 即删即增
                self.all_blocks.append([0 for column in range(self.all_columns)])
                self.score += 1
                break

    def block_move(self, move_position: int) -> None:
        """左右移动方块movePosition>0 代表向右移动一格 <0 代表向左移动一格"""
        for position in self.block:
            x = position[0] + self.current_column + move_position
            y = position[1] + self.current_row
            if x < 0 or x > self.all_columns - 1 or y > self.all_rows:
                # 说明方块左右移动出边界了
                return
            elif self.all_blocks[y][x] == 1:
                # 说明方块左右移动碰到方块了
                return
        else:
            self.current_column += move_position

    def rotate(self):
        """顺时针旋转方块"""
        for position in self.blocks[self.shape][(self.index + 1) % 4]:
            x = position[0] + self.current_column
            y = position[1] + self.current_row
            # print(x, y)
            if x < 0 or x > self.all_columns - 1 or y > self.all_rows:
                # 说明方块旋转时候出边界了
                return
            elif self.all_blocks[y][x] == 1:
                # 说明方块旋转时候碰到方块了
                return
        else:
            self.index += 1
            # print(self.blocks[self.shape][self.index % 4])
            self.block = self.blocks[self.shape][self.index % 4]

    def start(self):
        """开始游戏"""
        self.is_game_start = True
        self.is_game_over = False
        self.is_pause = False
        # 获取焦点
        self.setFocus()
        # 显示暂停按钮
        self.btn_pause.show()
        # 初始化
        self.init_settings()
        self.init_font()
        self.init_timer()
        # 获取方块
        self.next_block_dict = self.get_block()
        self.get_current_block()

    def pause(self):
        """游戏暂停"""
        self.is_pause = True
        self.drop_timer.disconnect()

    def resume(self):
        """游戏继续"""
        self.is_pause = False
        self.drop_timer.start(self.drop_interval)
        self.drop_timer.timeout.connect(self.block_drop)

    def game_over(self):
        """游戏结束"""
        self.is_game_over = True

    def paintEvent(self, event: QPaintEvent) -> None:
        """重写paintEvent, 使用QTimer, 每10ms调用一次"""
        self.painter = QPainter()
        self.painter.begin(self)  # 开始重绘

        if self.is_game_start is True:
            pen_color = QColor(255, 255, 255)  # 白色
            # backgroundColor = QColor(255, 192, 203)  # 粉色
            self.painter.setPen(QPen(pen_color, 2, Qt.SolidLine, Qt.RoundCap))     # 白色,
            self.pixmap = QPixmap("./icons/game_background.png")
            self.painter.drawPixmap(QRect(0, 0, self.screen_width, self.screen_height), self.pixmap)    # 背景图片
            self.painter.drawLine(self.screen_width - 300, 0, self.screen_width - 300, self.screen_height)   # 分割线

            # 绘制正在下落的方块
            for position in self.block:
                x = position[0] + self.current_column
                y = position[1] + self.current_row
                self.painter.drawPixmap(QRect(x * self.block_size, (self.all_rows - y) * self.block_size,
                                              self.block_size, self.block_size), QPixmap("./icons/block.png"))

            # 绘制静态方块
            for row in range(1, self.all_rows + 1):
                for column in range(self.all_columns):
                    if self.all_blocks[row][column] == 1:
                        self.painter.drawPixmap(QRect(column * self.block_size, (self.all_rows - row) * self.block_size,
                                                      self.block_size, self.block_size), QPixmap("./icons/fill_block.png"))

            # 绘制下一个出现的方块
            for position in self.next_block_dict["block"]:
                x = position[0] + 18.5  # 18.5是740px/40px(方块大小)
                y = position[1] + 12.5   # 7.5是500px/40px(方块大小) 从下往上
                self.painter.drawPixmap(QRect(int(x * self.block_size), int((self.all_rows - y) * self.block_size),
                                              self.block_size, self.block_size), QPixmap("./icons/block.png"))

            # 绘制得分情况
            self.painter.setFont(self.font)
            self.painter.drawText(self.screen_width - 250, 150, "Score: %d" % self.score)

        self.painter.end()    # 结束重绘

    def focusOutEvent(self, event: QFocusEvent) -> None:
        """焦点丢失事件"""
        # 如果游戏开始, 使焦点一直在这个窗口上
        if self.is_game_start is True:
            self.setFocus()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """重写keyPressEvent"""
        # 如果游戏结束或者游戏暂停则直接return
        if self.is_game_over or self.is_pause:
            return

        if event.key() == Qt.Key_A:
            self.block_move(-1)
        elif event.key() == Qt.Key_D:
            self.block_move(1)
        if event.key() == Qt.Key_W:
            self.rotate()
        if event.key() == Qt.Key_S:
            # 加速下降, 加速一个方格
            self.block_drop()
