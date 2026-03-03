# -*- coding: utf-8 -*-
"""
UI 覆盖层模块
在屏幕顶部中央显示手势状态图标
"""

import tkinter as tk
from typing import Optional

from logger import setup_logger

logger = setup_logger("ui_overlay")


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
            pass  # 非 Windows 系统可能不支持

        # 窗口大小和位置
        self.width = 200
        self.height = 80

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算位置（顶部中央）
        x = (screen_width - self.width) // 2
        y = 20  # 距离顶部 20 像素

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.configure(bg="white")

        # 创建内容框架
        self.frame = tk.Frame(self.root, bg="white", bd=0)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 图标标签
        self.icon_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI Emoji", 32),
            bg="white",
            fg="#888888"
        )
        self.icon_label.pack(pady=(5, 0))

        # 状态文字标签
        self.text_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#888888"
        )
        self.text_label.pack()

        # 初始状态
        self.set_state("idle")

        # 隐藏窗口（初始不显示）
        self.root.withdraw()

        logger.info("UI 覆盖层初始化完成")

    def set_state(self, state: str):
        """
        设置状态显示

        Args:
            state: "idle" / "ready" / "captured"
        """
        if state == "idle":
            # idle 状态隐藏窗口
            self.hide()
        elif state == "ready":
            self.icon_label.config(text="\u270B", fg="#4CAF50")  # 举起的手
            self.text_label.config(text="READY", fg="#4CAF50")
            self.show()
        elif state == "captured":
            self.icon_label.config(text="\U0001F4F7", fg="#2196F3")  # 相机
            self.text_label.config(text="Captured!", fg="#2196F3")
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
        """更新窗口（处理事件）"""
        self.root.update()

    def destroy(self):
        """销毁窗口"""
        self.root.destroy()
        logger.info("UI 覆盖层已销毁")
