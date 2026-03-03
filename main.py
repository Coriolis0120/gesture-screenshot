# -*- coding: utf-8 -*-
"""
手势截图主程序
通过摄像头检测手势变化（张开 -> 握拳），触发桌面截图
"""

import sys
import os
import time

# 添加 src 目录到 Python 路径（开发环境）
if not getattr(sys, 'frozen', False):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import cv2

from gesture_detector import GestureDetector
from logger import setup_logger
from screenshot import take_screenshot
from ui_overlay import StatusOverlay

# 配置
CAMERA_ID = 0  # 摄像头ID，默认为0
SCREENSHOT_COOLDOWN = 1.0  # 截图冷却时间（秒），防止连续触发
CAPTURED_DISPLAY_TIME = 1.5  # 截图成功显示时间（秒）

logger = setup_logger("main")


def main():
    """主程序入口"""
    logger.info("程序启动")

    # 初始化 UI 覆盖层（初始隐藏）
    overlay = StatusOverlay()

    # 初始化摄像头
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        logger.error("无法打开摄像头")
        overlay.destroy()
        print("错误：无法打开摄像头，请检查摄像头是否连接")
        return

    logger.info(f"摄像头已打开，ID: {CAMERA_ID}")

    # 初始化手势检测器
    detector = GestureDetector()

    # 上次截图时间
    last_screenshot_time = 0

    # 截图成功回调时间
    captured_until = 0

    print("=" * 50)
    print("手势截图程序已启动")
    print("操作说明：")
    print("  1. 对着摄像头张开手掌（激活）")
    print("  2. 握拳（触发截图）")
    print("  - 按 Ctrl+C 退出程序")
    print("=" * 50)

    try:
        while True:
            # 更新 UI（处理 tkinter 事件）
            overlay.update()

            # 读取帧
            ret, frame = cap.read()
            if not ret:
                logger.error("无法读取摄像头画面")
                break

            # 水平翻转（镜像效果）
            frame = cv2.flip(frame, 1)

            # 检测手势
            gesture, results, closed_count = detector.detect(frame)

            # 检查手势变化
            if detector.check_gesture_change(gesture, closed_count):
                current_time = time.time()
                # 检查冷却时间
                if current_time - last_screenshot_time >= SCREENSHOT_COOLDOWN:
                    logger.info("触发截图")
                    filepath = take_screenshot()
                    if filepath:
                        print(f"截图已保存: {filepath}")
                        overlay.set_state("captured")
                        captured_until = current_time + CAPTURED_DISPLAY_TIME
                    last_screenshot_time = current_time
                else:
                    logger.debug("截图冷却中，跳过")

            # 更新 UI 状态
            current_time = time.time()
            if captured_until > 0 and current_time < captured_until:
                # 仍在显示截图成功状态
                pass
            elif detector.state == "ready":
                overlay.set_state("ready")
            else:
                overlay.set_state("idle")

    except KeyboardInterrupt:
        logger.info("用户中断程序")

    finally:
        # 释放资源
        cap.release()
        detector.release()
        overlay.destroy()
        logger.info("程序正常退出")
        print("程序已退出")


if __name__ == "__main__":
    main()
