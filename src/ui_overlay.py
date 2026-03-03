# -*- coding: utf-8 -*-
"""
UI 覆盖层模块
在屏幕顶部中央显示手势状态图标（科技感设计）
"""

import tkinter as tk

from logger import setup_logger

logger = setup_logger("ui_overlay")

# 科技感配色
COLOR_READY = "#00E5FF"      # 青色（赛博朋克风）
COLOR_CAPTURED = "#FF4081"   # 粉红色
COLOR_BG = "#1A1A2E"         # 深色背景
COLOR_BORDER = "#00E5FF"     # 边框颜色


class StatusOverlay:
    """状态覆盖层 - 在屏幕顶部显示手势状态"""

    def __init__(self):
        """初始化透明覆盖窗口"""
        self.root = tk.Tk()

        # 窗口属性设置
        self.root.title("Gesture Status")
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes("-topmost", True)  # 始终置顶

        # 设置透明背景（Windows）
        try:
            self.root.attributes("-transparentcolor", "white")
        except tk.TclError:
            pass

        # 窗口大小（缩小）
        self.width = 120
        self.height = 50

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()

        # 计算位置（顶部中央）
        x = (screen_width - self.width) // 2
        y = 15  # 距离顶部 15 像素

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.configure(bg="white")

        # 外层框架（用于创建圆角效果）
        self.outer_frame = tk.Frame(self.root, bg="white", bd=0)
        self.outer_frame.pack(fill=tk.BOTH, expand=True)

        # 内层框架（深色背景）
        self.inner_frame = tk.Frame(
            self.outer_frame,
            bg=COLOR_BG,
            bd=2,
            relief=tk.SOLID,
            highlightbackground=COLOR_READY,
            highlightthickness=1
        )
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # 状态文字标签（使用等宽字体增加科技感）
        self.label = tk.Label(
            self.inner_frame,
            text="",
            font=("Consolas", 12, "bold"),
            bg=COLOR_BG,
            fg=COLOR_READY
        )
        self.label.pack(expand=True)

        # 初始状态
        self.set_state("idle")

        # 隐藏窗口
        self.root.withdraw()

        logger.info("UI 覆盖层初始化完成")

    def set_state(self, state: str):
        """
        设置状态显示

        Args:
            state: "idle" / "ready" / "captured"
        """
        if state == "idle":
            self.hide()
        elif state == "ready":
            self.label.config(text="[ READY ]", fg=COLOR_READY)
            self.inner_frame.config(
                highlightbackground=COLOR_READY
            )
            self.show()
        elif state == "captured":
            self.label.config(text="[ SNAP! ]", fg=COLOR_CAPTURED)
            self.inner_frame.config(
                highlightbackground=COLOR_CAPTURED
            )
            self.show()

        self.root.update()
        logger.debug(f"UI 状态更新: {state}")

    def show(self):
        """显示窗口"""
        self.root.deiconify()
        self.root.update()

    def hide(self):
        """隐藏窗口"""
        self.root.withdraw()
        self.root.update()

    def update(self):
        """更新窗口"""
        self.root.update()

    def destroy(self):
        """销毁窗口"""
        self.root.destroy()
        logger.info("UI 覆盖层已销毁")
