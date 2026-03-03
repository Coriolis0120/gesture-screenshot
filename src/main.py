"""
手势截图主程序
通过摄像头检测手势变化（张开 → 握拳），触发桌面截图
"""

import time

import cv2

from src.gesture_detector import GestureDetector
from src.logger import setup_logger
from src.screenshot import take_screenshot

# 配置
CAMERA_ID = 0  # 摄像头ID，默认为0
SCREENSHOT_COOLDOWN = 1.0  # 截图冷却时间（秒），防止连续触发

logger = setup_logger("main")


def main():
    """主程序入口"""
    logger.info("程序启动")

    # 初始化摄像头
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        logger.error("无法打开摄像头")
        print("错误：无法打开摄像头，请检查摄像头是否连接")
        return

    logger.info(f"摄像头已打开，ID: {CAMERA_ID}")

    # 初始化手势检测器
    detector = GestureDetector()

    # 上次截图时间
    last_screenshot_time = 0

    print("=" * 50)
    print("手势截图程序已启动")
    print("操作说明：")
    print("  - 张开手掌，然后握拳 → 触发截图")
    print("  - 按 'q' 键退出程序")
    print("=" * 50)

    try:
        while True:
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                logger.error("无法读取摄像头画面")
                break

            # 水平翻转（镜像效果）
            frame = cv2.flip(frame, 1)

            # 检测手势
            gesture, results = detector.detect(frame)

            # 绘制手部关键点
            frame = detector.draw_landmarks(frame, results)

            # 显示当前手势状态
            status_text = f"Gesture: {gesture if gesture else 'None'}"
            cv2.putText(
                frame, status_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

            # 检查手势变化
            if detector.check_gesture_change(gesture):
                current_time = time.time()
                # 检查冷却时间
                if current_time - last_screenshot_time >= SCREENSHOT_COOLDOWN:
                    logger.info("触发截图")
                    filepath = take_screenshot()
                    if filepath:
                        print(f"截图已保存: {filepath}")
                        # 在画面上显示提示
                        cv2.putText(
                            frame, "Screenshot Saved!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
                        )
                    last_screenshot_time = current_time
                else:
                    logger.debug("截图冷却中，跳过")

            # 显示画面
            cv2.imshow("Gesture Screenshot", frame)

            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q"):
                logger.info("用户按下 'q' 键，准备退出")
                break

    except KeyboardInterrupt:
        logger.info("用户中断程序")

    finally:
        # 释放资源
        cap.release()
        cv2.destroyAllWindows()
        detector.release()
        logger.info("程序正常退出")
        print("程序已退出")


if __name__ == "__main__":
    main()
