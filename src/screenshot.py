# -*- coding: utf-8 -*-
"""
截图模块
提供桌面截图功能，保存到 Windows 图片文件夹
"""

import os
from datetime import datetime
from typing import Optional

import pyautogui

from logger import setup_logger

logger = setup_logger("screenshot")

# 截图保存目录：Windows 图片文件夹下的 GestureScreenshots
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
SAVE_DIR = os.path.join(PICTURES_DIR, "GestureScreenshots")


def take_screenshot() -> Optional[str]:
    """
    截取当前桌面并保存到 Windows 图片文件夹

    Returns:
        截图文件路径，失败返回 None
    """
    try:
        # 确保保存目录存在
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            logger.info(f"创建截图目录: {SAVE_DIR}")

        # 生成文件名（带时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gesture_{timestamp}.png"
        filepath = os.path.join(SAVE_DIR, filename)

        # 截图
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        logger.info(f"截图保存成功: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"截图失败: {e}")
        return None
