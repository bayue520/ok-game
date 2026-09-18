import cv2
from ok import BaseTask
import random

class TestDrag(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "TestDrag"
        self.description = "测试找炮塔并拖动"

    def run(self):
        self.info_set("状态", "开始")
        self.log_info("=== 开始 ===")

        # 炮塔范围（模拟器 ADB 模式下的坐标）
        tower_x_min = 195
        tower_x_max = 235
        tower_y_min = 794
        tower_y_max = 880

        # 在炮塔范围内随机取点
        rx = random.randint(tower_x_min, tower_x_max)
        ry = random.randint(tower_y_min, tower_y_max)
        self.info_set("随机点", f"{rx}, {ry}")
        self.log_info(f"随机点：{rx}, {ry}")

        # 目标：一号窗
        target_x, target_y = 112, 835

        self.log_info("=== 准备 swipe ===")
        self.swipe(rx, ry, target_x, target_y, duration=0.5)
        self.log_info("=== swipe 完成 ===")

        self.info_set("状态", "拖动完成")