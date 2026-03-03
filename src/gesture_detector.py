"""
手势检测模块
使用 MediaPipe 检测手势状态（张开/握拳）
"""

from typing import Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

from src.logger import setup_logger

logger = setup_logger("gesture_detector")

# 手指关键点索引
# 拇指: 1-4, 食指: 5-8, 中指: 9-12, 无名指: 13-16, 小指: 17-20
FINGER_TIPS = [4, 8, 12, 16, 20]  # 指尖
FINGER_MCPS = [2, 5, 9, 13, 17]  # 指根（掌指关节）


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
        self.prev_gesture: Optional[str] = None
        logger.info("手势检测器初始化完成")

    def detect(self, frame: np.ndarray) -> Tuple[Optional[str], object]:
        """
        检测手势状态

        Args:
            frame: BGR 图像帧

        Returns:
            (手势状态, MediaPipe结果对象)
            手势状态: "open" / "fist" / None
        """
        # 转换颜色空间 BGR -> RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 检测手部
        results = self.hands.process(rgb_frame)

        gesture = None

        if results.multi_hand_landmarks:
            # 只处理第一只手
            hand_landmarks = results.multi_hand_landmarks[0]

            # 统计弯曲的手指数量
            closed_count = self._count_closed_fingers(hand_landmarks)

            # 判断手势
            if closed_count >= 4:
                gesture = "fist"
            else:
                gesture = "open"

            logger.debug(f"检测到手势: {gesture}, 弯曲手指数: {closed_count}")

        return gesture, results

    def _is_finger_closed(
        self,
        landmarks,
        finger_tip_idx: int,
        finger_mcp_idx: int
    ) -> bool:
        """
        判断单个手指是否弯曲

        通过比较指尖与指根的 y 坐标距离来判断
        （假设手是竖直向上的）

        Args:
            landmarks: MediaPipe 手部关键点
            finger_tip_idx: 指尖索引
            finger_mcp_idx: 指根索引

        Returns:
            True 表示手指弯曲
        """
        tip = landmarks.landmark[finger_tip_idx]
        mcp = landmarks.landmark[finger_mcp_idx]

        # 指尖到指根的距离
        distance = abs(tip.y - mcp.y)

        # 阈值判断（可根据实际情况调整）
        # 距离小于 0.1 认为是弯曲
        return distance < 0.1

    def _count_closed_fingers(self, landmarks) -> int:
        """
        统计弯曲的手指数量

        Args:
            landmarks: MediaPipe 手部关键点

        Returns:
            弯曲的手指数量 (0-5)
        """
        count = 0

        # 检查每个手指（拇指需要特殊处理）
        for i in range(1, 5):  # 食指、中指、无名指、小指
            if self._is_finger_closed(landmarks, FINGER_TIPS[i], FINGER_MCPS[i]):
                count += 1

        # 拇指判断（使用 x 坐标）
        thumb_tip = landmarks.landmark[FINGER_TIPS[0]]
        thumb_mcp = landmarks.landmark[FINGER_MCPS[0]]
        if abs(thumb_tip.x - thumb_mcp.x) < 0.05:
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

    def check_gesture_change(self, current_gesture: Optional[str]) -> bool:
        """
        检查手势是否从张开变为握拳

        Args:
            current_gesture: 当前手势状态

        Returns:
            True 表示发生了 open → fist 的变化
        """
        changed = False

        if current_gesture == "fist" and self.prev_gesture == "open":
            logger.info("手势变化: open → fist")
            changed = True

        # 更新上一帧状态
        self.prev_gesture = current_gesture

        return changed

    def release(self):
        """释放资源"""
        self.hands.close()
        logger.info("手势检测器资源已释放")
