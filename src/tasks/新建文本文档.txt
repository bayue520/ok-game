from ok import BaseTask
import random

class EnterGame(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "EnterGame"
        self.description = "点第五关进游戏"

    def run(self):
        self.info_set("状态", "准备点第五关")
        self.log_info("=== 准备点第五关 ===")

        # 第五关开始按钮坐标
        btn_x, btn_y = 330, 663

        # 点击位置随机（按钮范围内随机）
        # 按钮大概宽 100、高 40，在范围内随机
        rx = random.randint(btn_x - 30, btn_x + 30)
        ry = random.randint(btn_y - 10, btn_y + 10)
        self.info_set("点击位置", f"{rx}, {ry}")
        self.log_info(f"点击：{rx}, {ry}")

        self.click(rx, ry)

        self.info_set("状态", "已点击第五关")
        self.log_info("=== 点击完成 ===")