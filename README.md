# Gesture Screenshot

通过手势控制桌面截图的 Windows 工具。对着摄像头张开手掌激活，握拳触发截图。

## 功能

- 摄像头实时手势检测
- 张开手掌 → 握拳 = 截图
- 科技感 UI 状态提示
- 后台运行，不影响其他操作
- 打包成 exe，无需 Python 环境即可运行

## 安装


### 从源码运行

```bash
# 克隆仓库
git clone https://github.com/Coriolis0120/gesture-screenshot.git
cd gesture-screenshot

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 使用方法

1. 运行程序后，程序在后台静默运行
2. 对着摄像头**张开手掌**（激活）
3. 屏幕顶部会显示 `[ READY ]` 提示
4. **握拳**触发截图
5. 截图保存在 `C:\Users\<用户名>\Pictures\GestureScreenshots\`

## 退出程序

按 `Ctrl+C` 退出

## 打包

```bash
build.bat
```

打包后的 exe 文件在 `dist/` 目录下。

## 技术栈

- Python 3.10+
- OpenCV - 摄像头捕获
- MediaPipe - 手势识别
- PyAutoGUI - 桌面截图
- tkinter - UI 界面
- PyInstaller - 打包成 exe

## 项目结构

```
gesture-screenshot/
├── main.py              # 主程序入口
├── build.bat            # 打包脚本
├── requirements.txt     # 依赖列表
├── src/
│   ├── gesture_detector.py  # 手势检测模块
│   ├── screenshot.py        # 截图模块
│   ├── ui_overlay.py        # UI 覆盖层
│   └── logger.py            # 日志模块
└── screenshots/         # 截图保存目录（开发时）
```

## 日志

日志保存在 `C:\Users\<用户名>\Pictures\GestureScreenshots\logs\`

## License

MIT
