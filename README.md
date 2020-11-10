---
typora-copy-images-to: upload

---

## PyQt5-Tetris

### PyQt5俄罗斯方块，PyQt5-Tetris，基于PyQt5写的一个小游戏

<br>

#### 源码依赖

- windows操作系统

- 安装python3以及pip

```
pip install PyQt5
```

#### 功能

- 可以播放音乐, 把MP3文件放入BackgroundMusic即可 -> 边玩游戏边听歌是一种享受
- 实现了俄罗斯方块的基本功能, 可以暂停游戏 -> 急事, 游戏玩得正兴, 不怕有暂停功能
- 增加了游戏消除方块的音效 -> 增加玩游戏的快感
- 游戏结束可以重新开始 -> 游戏玩得不够尽兴, 游戏结束可以重新开始


#### 使用方法

1、 直接运行main.py文件

2、 终端打开进入到相应目录下执行

```
python main.py
```

#### 缺点

- 不能拖拽游戏窗口
- 需要手动添加想听的音乐
- 界面做得不够好看（不会使用Qt Designer QWQ）

#### 已知BUG

- 点击按钮后, 键盘事件会失去监听，需要再次点击游戏界面才可以恢复（希望大佬们可以提供解决方案）


#### 下面是代码运行的效果(如果gif加载不出来， 下面可能没有内容)


![example](C:%5CUsers%5CLUO%5CDesktop%5Cexample.gif)
