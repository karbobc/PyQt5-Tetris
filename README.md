<h2 align="center">PyQt5-Tetris</h2>

<p align="center">
    <a href="https://img.shields.io/github/pipenv/locked/python-version/karbob666/pyqt5-tetris">
        <img src="https://img.shields.io/github/pipenv/locked/python-version/karbob666/pyqt5-tetris" alt="python v3.8" />
    </a>
    <a href="https://img.shields.io/github/license/karbob666/PyQt5-Tetris">
        <img src="https://img.shields.io/github/license/karbob666/PyQt5-Tetris" alt="GPL-3.0" />
    </a>
</p>

## 📝 功能

- 🎵 播放音乐
- ⏸︎ 暂停游戏
- 🎸 消除方块的音效
- 🖱️ 窗口自由拖拽

## ⌨️ 安装和运行

### 1. 使用`pip`

```shell
# 克隆仓库
git clone https://github.com/karbob666/PyQt5-Tetris.git

# 进入到项目
cd PyQt5-Tetris

# 使用pip安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

### 2. 使用`pipenv`

```shell
# 克隆仓库
git clone https://github.com/karbob666/PyQt5-Tetris.git

# 进入到项目
cd PyQt5-Tetris

# 使用pipenv安装依赖
pipenv sync

# 运行
pipenv run start
```

### 3. 按键说明

- `A` - 向左移动
- `D`- 向右移动
- `W` - 变形
- `S` - 加速下降
- `P` - 暂停
- `ESC` - 退出程序

## 📦 PyInstaller 打包

### 1. 使用`pip`

```shell
# 安装依赖
pip install -r requirements-dev.txt

# 打包，打包成功之后exe文件在dist文件夹下
pyinstaller main.spec
```

### 2. 使用`pipenv`

```shell
# 安装依赖
pipenv install --dev

# 打包，打包成功之后exe文件在dist文件夹下
pipenv run build
```

## 🖼️ 页面展示

![image-20220427143916101](https://karbob-bucket.oss-cn-hangzhou.aliyuncs.com/markdown/image-20220427143916101.png)

![image-20220427144006320](https://karbob-bucket.oss-cn-hangzhou.aliyuncs.com/markdown/image-20220427144006320.png)

## ✅ Todo

- 📄 游戏存档
- ⚙️ 添加设置

## 📜 许可证

PyQt5-Tetris使用 [GPL-v3.0](https://opensource.org/licenses/GPL-3.0) 协议开源，请遵守开源协议。