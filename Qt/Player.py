"""
...@coding: UTF-8
...@version: python 3.8x
...@fileName: Player.py
...@author: Karbob
...@date: 2020-11-04
"""

import os
from typing import List
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


class Player(QMediaPlayer):

    player: QMediaPlayer                # 播放器
    play_list: QMediaPlaylist           # 播放列表
    music_source_list: List[str]        # 音频路径列表
    MUSIC_DIR = "./BackgroundMusic"     # 存放音乐文件夹

    def __init__(self, parent=None) -> None:
        super(Player, self).__init__(parent)

        self.get_music_source()
        self.init_player()
        self.create_play_list()
        self.player.play()

    def get_music_source(self) -> None:
        """获取音乐文件路径"""
        self.music_source_list = list()
        for src in os.listdir(self.MUSIC_DIR):
            self.music_source_list.append("{}/{}".format(self.MUSIC_DIR, src))

    def init_player(self) -> None:
        """初始化播放器"""
        self.player = QMediaPlayer(self)  # 创建播放器
        self.play_list = QMediaPlaylist(self.player)  # 播放列表
        self.play_list.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)  # 播放模式
        """
        QMediaPlaylist.CurrentItemOnce       0->播放一次
        QMediaPlaylist.CurrentItemInLoop     1->单曲循环
        QMediaPlaylist.Sequential            2->顺序播放
        QMediaPlaylist.Loop                  3->列表循环
        QMediaPlaylist.Random                4->随机播放
        """

    def create_play_list(self) -> None:
        """创建播放列表"""
        self.play_list.clear()
        for path in self.music_source_list:
            content = QMediaContent(QUrl.fromLocalFile(path))
            self.play_list.addMedia(content)
        # 创建播放列表
        self.player.setPlaylist(self.play_list)
        # print(self.player.currentMedia().canonicalUrl().path())  # 输出音乐文件路径

    def next_music(self) -> None:
        """播放下一首音乐"""
        if self.play_list.currentIndex() == len(self.music_source_list) - 1:
            index = 0
        else:
            index = self.play_list.currentIndex() + 1

        self.play_list.setCurrentIndex(index)
        self.player.play()

    def previous_music(self) -> None:
        """播放前一首音乐"""
        if self.play_list.currentIndex() == 0:
            index = len(self.music_source_list) - 1
        else:
            index = self.play_list.currentIndex() - 1

        self.play_list.setCurrentIndex(index)
        self.player.play()

    def mute(self) -> None:
        """静音"""
        self.player.setMuted(True)

    def cancel_mute(self) -> None:
        """取消静音"""
        self.player.setMuted(False)
