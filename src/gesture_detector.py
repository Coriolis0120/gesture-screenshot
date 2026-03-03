# -*- coding: utf-8 -*-
"""
手势检测模块
使用 MediaPipe 检测手势状态（张开/握拳）

状态机制：
- idle: 空闲，等待检测到完全张开的手掌
- ready: 准备，已检测到张开手掌，等待握拳
- trigger: 触发，检测到握拳，触发截图
"""

from typing import Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

from logger import setup_logger

logger = setup_logger("gesture_detector")

# 手指关键点索引
# 拇指: 1-4, 食指: 5-8, 中指: 9-12, 无名指: 13-16, 小指: 17-20
FINGER_TIPS = [4, 8, 12, 16, 20]  # 指尖
FINGER_MCPS = [2, 5, 9, 13, 17]  # 指根（掌指关节）
FINGER_PIPS = [3, 6, 10, 14, 18]  # 近端指间关节

# 手势判断阈值
OPEN_THRESHOLD = 1  # 弯曲手指数 <= 此值认为手掌张开
FIST_THRESHOLD = 4  # 弯曲手指数 >= 此值认为握拳


class GestureDetector:
    """手势检测器"""

    def __init__(self):
        """初始化 MediaPipe Hands"""
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # 状态：idle -> ready -> trigger
        self.state = "idle"
        self.prev_closed_count = 0

        logger.info("手势检测器初始化完成")

    def detect(self, frame: np.ndarray) -> Tuple[Optional[str], object, int]:
        """
        检测手势状态

        Args:
            frame: BGR 图像帧

        Returns:
            (手势状态, MediaPipe结果对象, 弯曲手指数)
            手势状态: "open" / "fist" / None
        """
        # 转换颜色空间 BGR -> RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 检测手部
        results = self.hands.process(rgb_frame)

        gesture = None
        closed_count = 0

        if results.multi_hand_landmarks:
            # 只处理第一只手
            hand_landmarks = results.multi_hand_landmarks[0]

            # 统计弯曲的手指数量
            closed_count = self._count_closed_fingers(hand_landmarks)

            # 判断手势（更严格的条件）
            if closed_count <= OPEN_THRESHOLD:
                gesture = "open"
            elif closed_count >= FIST_THRESHOLD:
                gesture = "fist"
            # 中间状态不算任何手势

            logger.debug(f"检测到手势: {gesture}, 弯曲手指数: {closed_count}, 状态: {self.state}")

        return gesture, results, closed_count

    def _is_finger_closed(
        self,
        landmarks,
        finger_tip_idx: int,
        finger_mcp_idx: int,
        finger_pip_idx: int
    ) -> bool:
        """
        判断单个手指是否弯曲

        手掌朝向摄像头时：
        - 手指伸直：指尖在画面上方（y 值小）
        - 手指弯曲：指尖在画面下方（y 值大）

        Args:
            landmarks: MediaPipe 手部关键点
            finger_tip_idx: 指尖索引
            finger_mcp_idx: 指根索引
            finger_pip_idx: 近端指间关节索引

        Returns:
            True 表示手指弯曲
        """
        tip = landmarks.landmark[finger_tip_idx]
        pip = landmarks.landmark[finger_pip_idx]
        mcp = landmarks.landmark[finger_mcp_idx]

        # 手掌朝向摄像头时：
        # - 伸直：tip.y < pip.y（指尖在上）
        # - 弯曲：tip.y > pip.y（指尖在下）
        is_closed = tip.y > pip.y

        return is_closed

    def _count_closed_fingers(self, landmarks) -> int:
        """
        统计弯曲的手指数量

        Args:
            landmarks: MediaPipe 手部关键点

        Returns:
            弯曲的手指数量 (0-5)
        """
        count = 0

        # 检查四指（食指、中指、无名指、小指）
        for i in range(1, 5):
            if self._is_finger_closed(
                landmarks,
                FINGER_TIPS[i],
                FINGER_MCPS[i],
                FINGER_PIPS[i]
            ):
                count += 1

        # 拇指判断（使用 x 坐标）
        thumb_tip = landmarks.landmark[FINGER_TIPS[0]]
        thumb_ip = landmarks.landmark[FINGER_PIPS[0]]
        # 拇指弯曲时，指尖 x 坐标更靠近手掌中心
        if abs(thumb_tip.x - thumb_ip.x) < 0.03:
            count += 1

        return count

    def draw_landmarks(self, frame: np.ndarray, results) -> np.ndarray:
        """
        在图像上绘制手部关键点

        Args:
            frame: BGR 图像帧
            results: MediaPipe 检测结果

        Returns:
            绘制后的图像
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def check_gesture_change(self, gesture: Optional[str], closed_count: int) -> bool:
        """
        检查手势是否触发截图

        状态转换：
        - idle + 检测到张开手掌 -> ready
        - ready + 检测到握拳 -> trigger（触发截图）-> idle
        - 其他情况保持当前状态

        Args:
            gesture: 当前手势状态
            closed_count: 当前弯曲手指数

        Returns:
            True 表示触发截图
        """
        trigger = False

        if gesture == "open" and closed_count <= OPEN_THRESHOLD:
            # 检测到完全张开的手掌
            if self.state != "ready":
                self.state = "ready"
                logger.info(f"状态变化: -> ready (检测到张开手掌, 弯曲: {closed_count})")

        elif gesture == "fist" and closed_count >= FIST_THRESHOLD:
            # 检测到完全握拳
            if self.state == "ready":
                # 只有在 ready 状态下才触发
                self.state = "idle"
                logger.info(f"状态变化: ready -> trigger -> idle (检测到握拳, 弯曲: {closed_count})")
                trigger = True

        elif gesture is None:
            # 没有检测到手，重置状态
            if self.state != "idle":
                logger.info("状态变化: -> idle (未检测到手)")
            self.state = "idle"

        self.prev_closed_count = closed_count
        return trigger

    def get_state_text(self) -> str:
        """获取当前状态的文本描述"""
        if self.state == "ready":
            return "READY - Make a fist to screenshot!"
        return "Show open palm to activate"

    def release(self):
        """释放资源"""
        self.hands.close()
        logger.info("手势检测器资源已释放")
