# -*- coding: utf-8 -*-
"""
日志配置模块
提供统一的日志记录功能，同时输出到控制台和文件
"""

import logging
import os
from datetime import datetime

# 日志保存目录：与截图相同的用户目录
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
LOG_DIR = os.path.join(PICTURES_DIR, "GestureScreenshots", "logs")


def setup_logger(name: str = "gesture_screenshot") -> logging.Logger:
    """
    配置并返回日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        配置好的 Logger 对象
    """
    # 创建日志目录
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出
    log_filename = datetime.now().strftime("%Y%m%d") + ".log"
    log_filepath = os.path.join(LOG_DIR, log_filename)
    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
