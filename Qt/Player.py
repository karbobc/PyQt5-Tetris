"""
...@coding: UTF-8
...@version: python 3.8x
...@version: Player.py
...@author: Luo
...@date: 2020-11-04
"""

import os
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

class Player(QMediaPlayer):

    player = None       # 播放器
    playList = None     # 播放列表
    source = None       # 音频路径
    content = None      # 音频内容
    musicSource = []    # 音频路劲列表
    MUSIC_PATH = './BackgroundMusic'

    def __init__(self, parent=None):
        super(Player, self).__init__(parent)

        self.getMusicSource()
        self.initPlayer()
        self.createPlayList()
        self.player.play()

    def getMusicSource(self):
        """获取音乐文件路径"""
        for src in os.listdir(self.MUSIC_PATH):
            self.musicSource.append('{}/{}'.format(self.MUSIC_PATH, src))

    def initPlayer(self):
        """初始化播放器"""
        self.player = QMediaPlayer(self)  # 创建播放器
        self.playList = QMediaPlaylist(self.player)  # 播放列表
        self.playList.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)  # 播放模式
        """
        QMediaPlaylist.CurrentItemOnce       0->播放一次
        QMediaPlaylist.CurrentItemInLoop     1->单曲循环
        QMediaPlaylist.Sequential            2->顺序播放
        QMediaPlaylist.Loop                  3->列表循环
        QMediaPlaylist.Random                4->随机播放
        """

    def createPlayList(self):
        """创建播放列表"""
        self.playList.clear()
        for path in self.musicSource:
            self.content = QMediaContent(QUrl.fromLocalFile(path))
            self.playList.addMedia(self.content)
        self.player.setPlaylist(self.playList)  # 创建播放列表
        # print(self.player.currentMedia().canonicalUrl().path())  # 输出音乐文件路径

    def nextMusic(self):
        """播放下一首音乐"""
        if self.playList.currentIndex() == len(self.musicSource) - 1:
            index = 0
        else:
            index = self.playList.currentIndex() + 1

        self.playList.setCurrentIndex(index)
        self.player.play()

    def previousMusic(self):
        """播放前一首音乐"""
        if self.playList.currentIndex() == 0:
            index = len(self.musicSource) - 1
        else:
            index = self.playList.currentIndex() - 1

        self.playList.setCurrentIndex(index)
        self.player.play()

    def mute(self):
        """静音"""
        self.player.setMuted(True)

    def cancelMute(self):
        """取消静音"""
        self.player.setMuted(False)