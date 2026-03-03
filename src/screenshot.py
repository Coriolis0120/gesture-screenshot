"""
截图模块
提供桌面截图功能
"""

import os
from datetime import datetime
from typing import Optional

import pyautogui

from src.logger import setup_logger

logger = setup_logger("screenshot")


def take_screenshot(save_dir: str = "screenshots") -> Optional[str]:
    """
    截取当前桌面并保存

    Args:
        save_dir: 截图保存目录

    Returns:
        截图文件路径，失败返回 None
    """
    try:
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logger.info(f"创建截图目录: {save_dir}")

        # 生成文件名（带时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)

        # 截图
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        logger.info(f"截图保存成功: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"截图失败: {e}")
        return None
