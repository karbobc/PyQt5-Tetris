"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: Tetris.py
...@author: Karbob
...@date: 2020-11-04
"""

import random
from .Player import Player
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QRect, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QPen, QPainter, QColor, QFont, QFontDatabase


class Tetris(QWidget):

    screenWidth = None          # 窗口宽度
    screenHeight = None         # 窗口高度
    isGameStart = None          # 游戏是否开始
    isGameOver = None           # 游戏是否结束
    isPause = None              # 游戏是否暂停
    pauseButton = None          # 暂停游戏按钮
    resumeButton = None         # 继续游戏按钮
    restartButton = None        # 重新开始游戏按钮
    gameOverImage = None        # 游戏结束时显示的图片
    blockSize = None            # 一个方块的大小(像素px)
    allRows = None              # 所有的行
    allColumns = None           # 所有的列
    allBlock = None             # 二维数组, 记录方块
    currentRow = None           # 当前行
    currentColumn = None        # 当前列
    dropTimer = None            # 方块下降的定时器
    updateTimer = None          # 屏幕更新的定时器
    removeBlockTimer = None     # 消除方块的定时器
    dropInterval = None         # 方块下降定时器的时间间隔
    updateInterval = None       # 屏幕更新定时器的时间间隔
    removeBlockInterval = None  # 消除方块定时器的时间间隔
    blocks = None               # 枚举所有的方块
    blockDict = None            # 存储方块属性的字典
    nextBlockDict = None        # 存储下一个方块属性的字典
    block = None                # 当前的方块
    shape = None                # 当前方块的类型
    index = None                # 当前方块类型的下标
    score = None                # 得分情况
    pixmap = None               # 临时存储图片路径
    paint = None                # 画笔
    font = None                 # 字体

    def __init__(self, parent=None):
        super(Tetris, self).__init__(parent)

        self.screenWidth = 900
        self.screenHeight = 800
        self.setFocusPolicy(Qt.StrongFocus)         # 设置焦点, 监听键盘
        self.resize(self.screenWidth, self.screenHeight)

        self.initButton()
        self.initImage()

    def initButton(self):
        """初始化重新开始游戏的按钮"""
        # 暂停游戏按钮
        self.pauseButton = QPushButton(self)
        self.pauseButton.setObjectName('pauseButton')
        self.pauseButton.setShortcut('P')
        self.pauseButton.setToolTip('暂停')  # 悬停在按钮上的提示->暂停
        self.pauseButton.move(self.screenWidth - 210, 5)  # 按钮的位置
        self.pauseButton.hide()  # 默认隐藏
        self.pauseButton.clicked.connect(lambda: {
            self.pause(),
            self.pauseButton.hide(),
            self.resumeButton.show(),
        })

        # 继续游戏按钮
        self.resumeButton = QPushButton(self)
        self.resumeButton.setObjectName('resumeButton')
        self.resumeButton.setToolTip('继续')  # 悬停在按钮上的提示->继续
        self.resumeButton.move(self.screenWidth - 210, 5)  # 按钮的位置
        self.resumeButton.hide()  # 默认隐藏
        self.resumeButton.clicked.connect(lambda: {
            self.resume(),
            self.resumeButton.hide(),
            self.pauseButton.show(),
        })

        # 重新开始游戏按钮
        self.restartButton = QPushButton(self)
        self.restartButton.setObjectName('restartButton')
        self.restartButton.move(self.screenWidth // 2 - 200, self.screenHeight // 2 - 50)
        self.restartButton.hide()       # 默认隐藏
        self.restartButton.clicked.connect(self.gameOver)

    def initImage(self):
        """初始化游戏结束的图片"""
        self.gameOverImage = QLabel(self)
        self.gameOverImage.setPixmap(QPixmap('./icons/game_over.png'))
        self.gameOverImage.move(self.screenWidth // 24, self.screenHeight // 4)
        self.gameOverImage.hide()   # 默认隐藏

    def initSetting(self):
        """初始化方块的一些初始值"""
        self.blocks = {
            'L Shape': [[[0, 0], [0, -1], [0, -2], [1, -2]], [[-1, -1], [0, -1], [1, -1], [-1, -2]],
                        [[-1, 0], [0, 0], [0, -1], [0, -2]], [[-1, -1], [0, -1], [1, -1], [1, 0]]],
            'J Shape': [[[0, 0], [0, -1], [0, -2], [-1, -2]], [[-1, 0], [-1, -1], [0, -1], [1, -1]],
                        [[0, 0], [1, 0], [0, -1], [0, -2]], [[-1, -1], [0, -1], [1, -1], [1, -2]]],
            'Z Shape': [[[-1, 0], [0, 0], [0, -1], [1, -1]], [[0, 0], [0, -1], [-1, -1], [-1, -2]],
                        [[-1, 0], [0, 0], [0, -1], [1, -1]], [[0, 0], [0, -1], [-1, -1], [-1, -2]]],
            'S Shape': [[[-1, 0], [-1, -1], [0, -1], [0, -2]], [[0, 0], [1, 0], [-1, -1], [0, -1]],
                        [[-1, 0], [-1, -1], [0, -1], [0, -2]], [[0, 0], [1, 0], [-1, -1], [0, -1]]],
            'O Shape': [[[-1, 0], [0, 0], [-1, -1], [0, -1]], [[-1, 0], [0, 0], [-1, -1], [0, -1]],
                        [[-1, 0], [0, 0], [-1, -1], [0, -1]], [[-1, 0], [0, 0], [-1, -1], [0, -1]]],
            'I Shape': [[[0, 0], [0, -1], [0, -2], [0, -3]], [[-2, -1], [-1, -1], [0, -1], [1, -1]],
                        [[0, 0], [0, -1], [0, -2], [0, -3]], [[-2, -1], [-1, -1], [0, -1], [1, -1]]],
            'T Shape': [[[-1, -1], [0, -1], [1, -1], [0, -2]], [[0, 0], [-1, -1], [0, -1], [0, -2]],
                        [[0, 0], [-1, -1], [0, -1], [1, -1]], [[0, 0], [0, -1], [1, -1], [0, -2]]]
        }
        self.score = 0
        self.blockSize = 40     # 方块的大小
        self.allRows = 20       # 总共20行
        self.allColumns = 15    # 总共15列
        self.currentRow = self.allRows + 4   # +4行是用来放置待出现的方块的
        self.currentColumn = self.allColumns // 2
        self.allBlock = [[0 for row in range(self.allColumns)] for column in range(self.allRows + 5)]
        self.allBlock[0] = [1 for column in range(self.allColumns)]    # 用来判断方块是否到底
        # print(self.allBlock)

    def initFont(self):
        """初始化字体"""
        # 使用本地字体
        fontID = QFontDatabase.addApplicationFont('./Font/Consolas Italic.ttf')
        self.font = QFont()
        self.font.setFamily(QFontDatabase.applicationFontFamilies(fontID)[0])
        self.font.setItalic(True)   # 斜体
        self.font.setBold(True)     # 粗体
        self.font.setPixelSize(40)  # 字体大小

    def initTimer(self):
        """初始化定时器"""
        # 方块下降的定时器
        self.dropTimer = QTimer(self)
        self.dropInterval = 500     # 每0.5秒下降一格
        self.dropTimer.start(self.dropInterval)
        self.dropTimer.timeout.connect(self.blockDrop)

        # paintEvent更新的定时器
        self.updateTimer = QTimer(self)
        self.updateInterval = 10
        self.updateTimer.start(self.updateInterval)
        self.updateTimer.timeout.connect(self.update)

        # 消除方块的定时器
        self.removeBlockTimer = QTimer(self)
        self.removeBlockInterval = 150
        self.removeBlockTimer.start(self.removeBlockInterval)
        self.removeBlockTimer.timeout.connect(self.removeBlock)

    def getBlock(self):
        """获取方块"""
        shape = random.choice(list(self.blocks.keys()))     # 选择随机方块的类型
        index = random.randint(0, 3)
        # if shape == 'L Shape' and index == 3:
        #     pass
        block = self.blocks[shape][index]
        blockDict = {
            'shape': shape,
            'index': index,
            'block': block,
        }
        return blockDict

    def getCurrentBlock(self):
        """获取目前的方块"""
        self.blockDict = self.nextBlockDict
        self.shape = self.blockDict['shape']
        self.index = self.blockDict['index']
        self.block = self.blockDict['block']
        self.nextBlockDict = self.getBlock()

    def blockDrop(self):
        """每运行一次, 方块下降一格, 通过QTimer每隔一定时间运行一次"""
        for position1 in self.block:
            x = position1[0] + self.currentColumn    # x->column
            y = position1[1] + self.currentRow       # y->row
            # print(x, y)
            if self.allBlock[y - 1][x] == 1:
                for position2 in self.block:
                    self.allBlock[position2[1] + self.currentRow][position2[0] + self.currentColumn] = 1
                break
        else:
            # 下落方块没有接触到其他方块或者没有到底, 继续下降
            self.currentRow -= 1
            return

        # 判断游戏结束
        if 1 in self.allBlock[self.allRows]:
            self.pause()
            self.update()
            self.removeBlockTimer.disconnect()
            self.updateTimer.disconnect()
            self.pauseButton.hide()
            self.gameOverImage.show()
            self.restartButton.show()
            return

        # 方块下落完成, 获取下一个方块
        self.getCurrentBlock()
        self.currentRow = self.allRows + 4
        self.currentColumn = self.allColumns // 2

    def removeBlock(self):
        """消除方块"""
        # 叠满一行时消除方块, 从上往下消除
        for row in range(self.allRows, 0, -1):
            if 0 not in self.allBlock[row]:
                # 消除方块时触发音效, 消除一行触发一次
                player = QMediaPlayer(self)
                player.setMedia(QMediaContent(QUrl.fromLocalFile('./AudioFrequency/dingdong.mp3')))
                player.play()

                self.allBlock.pop(row)  # 即删即增
                self.allBlock.append([0 for column in range(self.allColumns)])
                self.score += 1

                break

    def blockMove(self, movePosition):
        """左右移动方块movePosition>0 代表向右移动一格 <0 代表向左移动一格"""
        for position in self.block:
            x = position[0] + self.currentColumn + movePosition
            y = position[1] + self.currentRow
            if x < 0 or x > self.allColumns - 1 or y > self.allRows:
                # 说明方块左右移动出边界了
                return
            elif self.allBlock[y][x] == 1:
                # 说明方块左右移动碰到方块了
                return
        else:
            self.currentColumn += movePosition

    def rotate(self):
        """顺时针旋转方块"""
        for position in self.blocks[self.shape][(self.index + 1) % 4]:
            x = position[0] + self.currentColumn
            y = position[1] + self.currentRow
            # print(x, y)
            if x < 0 or x > self.allColumns - 1 or y > self.allRows:
                # 说明方块旋转时候出边界了
                return
            elif self.allBlock[y][x] == 1:
                # 说明方块旋转时候碰到方块了
                return
        else:
            self.index += 1
            # print(self.blocks[self.shape][self.index % 4])
            self.block = self.blocks[self.shape][self.index % 4]

    def start(self):
        """开始游戏"""
        self.isGameStart = True
        self.isGameOver = False
        self.isPause = False
        self.pauseButton.show()
        self.initSetting()
        self.initFont()
        self.initTimer()
        self.nextBlockDict = self.getBlock()
        self.getCurrentBlock()

    def pause(self):
        """游戏暂停"""
        self.isPause = True
        self.dropTimer.disconnect()

    def resume(self):
        """游戏继续"""
        self.isPause = False
        self.dropTimer.start(self.dropInterval)
        self.dropTimer.timeout.connect(self.blockDrop)

    def gameOver(self):
        """游戏结束"""
        self.isGameOver = True

    def paintEvent(self, event):
        """重写paintEvent, 使用QTimer, 每10ms调用一次"""
        self.paint = QPainter(self)
        self.paint.begin(self)  # 开始重绘

        if self.isGameStart is True:
            penColor = QColor(255, 255, 255)  # 白色
            # backgroundColor = QColor(255, 192, 203)  # 粉色
            self.paint.setPen(QPen(penColor, 2, Qt.SolidLine, Qt.RoundCap))     # 白色,
            self.pixmap = QPixmap('./icons/game_background.png')
            self.paint.drawPixmap(QRect(0, 0, self.screenWidth, self.screenHeight), self.pixmap)    # 背景图片
            self.paint.drawLine(self.screenWidth - 300, 0, self.screenWidth - 300, self.screenHeight)   # 分割线

            # 绘制正在下落的方块
            for position in self.block:
                x = position[0] + self.currentColumn
                y = position[1] + self.currentRow
                self.paint.drawPixmap(QRect(x * self.blockSize, (self.allRows - y) * self.blockSize,
                                            self.blockSize, self.blockSize), QPixmap('./icons/block.png'))

            # 绘制静态方块
            for row in range(1, self.allRows + 1):
                for column in range(self.allColumns):
                    if self.allBlock[row][column] == 1:
                        self.paint.drawPixmap(QRect(column * self.blockSize, (self.allRows - row) * self.blockSize,
                                                    self.blockSize, self.blockSize), QPixmap('./icons/fill_block.png'))

            # 绘制下一个出现的方块
            for position in self.nextBlockDict['block']:
                x = position[0] + 18.5  # 18.5是740px/40px(方块大小)
                y = position[1] + 12.5   # 7.5是500px/40px(方块大小) 从下往上
                self.paint.drawPixmap(QRect(int(x * self.blockSize), int((self.allRows - y) * self.blockSize),
                                            self.blockSize, self.blockSize), QPixmap('./icons/block.png'))

            # 绘制得分情况
            self.paint.setFont(self.font)
            self.paint.drawText(self.screenWidth - 250, 150, 'Score: %d' % self.score)

        self.paint.end()    # 结束重绘

    def keyPressEvent(self, event):
        """重写keyPressEvent"""
        if self.isGameOver is False and self.isPause is False:
            if event.key() == Qt.Key_A:
                self.blockMove(-1)
            elif event.key() == Qt.Key_D:
                self.blockMove(1)
            if event.key() == Qt.Key_W:
                self.rotate()
            if event.key() == Qt.Key_S:
                # 加速下降, 加速一个方格
                self.blockDrop()
