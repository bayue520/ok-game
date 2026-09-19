import cv2
import numpy as np
import gc
import os
from ok import BaseTask
from ultralytics import YOLO
import random


class AutoBattle(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "AutoBattle"
        self.description = "自动战斗"
        self.model = None

    def run(self):
        import global_state
        global_state.stop_flag = False

        self.info_set("状态", "开始")
        self.log_info("=== 开始 ===")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        model_path = os.path.join(BASE_DIR, "best.pt")
        tpl_path = os.path.join(BASE_DIR, "tpl.png")
        zero_path = os.path.join(BASE_DIR, "zero.png")
        retry_path = os.path.join(BASE_DIR, "retry.png")

        self.log_info(f"BASE_DIR = {BASE_DIR}")
        self.log_info(f"model_path = {model_path}, exists = {os.path.exists(model_path)}")
        self.log_info(f"tpl_path = {tpl_path}, exists = {os.path.exists(tpl_path)}")
        self.log_info(f"zero_path = {zero_path}, exists = {os.path.exists(zero_path)}")
        self.log_info(f"retry_path = {retry_path}, exists = {os.path.exists(retry_path)}")

        self.model = YOLO(model_path)

        tpl = cv2.imread(tpl_path)
        zero_tpl = cv2.imread(zero_path)
        retry_tpl = cv2.imread(retry_path)
        if tpl is None or zero_tpl is None or retry_tpl is None:
            self.info_set("状态", "模板没读到")
            self.log_info(f"tpl is None: {tpl is None}")
            self.log_info(f"zero_tpl is None: {zero_tpl is None}")
            self.log_info(f"retry_tpl is None: {retry_tpl is None}")
            return

        self.log_info("=== 点第五关 ===")
        self.click(330, 663)

        self.info_set("状态", "等炮塔出现")
        box = None
        for i in range(60):
            if global_state.stop_flag:
                return
            retry_box = self.find_one(template=retry_tpl, threshold=0.7)
            self.log_info(f"[等炮塔] retry_box = {retry_box}")
            if retry_box is not None:
                self.info_set("状态", "检测到重新挑战，点击")
                self.click_box(retry_box)
                self.sleep(2)
                continue
            box = self.find_one(template=tpl, threshold=0.4)
            self.log_info(f"[等炮塔] tpl_box = {box}")
            if box is not None:
                break
            self.sleep(0.5)

        if box is None:
            self.info_set("状态", "没等到炮塔")
            return

        cx = box.x + box.width // 2
        cy = box.y + box.height // 2
        rx = cx + random.randint(-10, 10)
        ry = cy + random.randint(-10, 10)
        self.swipe(rx, ry, 112, 835, duration=0.5)
        self.sleep(1)
        self.info_set("状态", "已在一号窗")

        self.info_set("状态", "先去三号打 1 秒")
        tpl_box = self.find_one(template=tpl, threshold=0.4)
        if tpl_box is not None:
            tx = tpl_box.x + tpl_box.width // 2
            ty = tpl_box.y + tpl_box.height // 2
            self.swipe(tx, ty, 367, 835, duration=0.5)
            self.sleep(1)
            tpl_box = self.find_one(template=tpl, threshold=0.4)
            if tpl_box is not None:
                tx = tpl_box.x + tpl_box.width // 2
                ty = tpl_box.y + tpl_box.height // 2
                self.swipe(tx, ty, 112, 835, duration=0.5)
        self.sleep(0.5)
        self.info_set("状态", "回一号窗")

        current_window = 1
        phase = 2

        while not global_state.stop_flag:
            frame = self.frame
            if frame is None:
                self.sleep(0.5)
                continue

            retry_box = self.find_one(template=retry_tpl, threshold=0.7)
            self.log_info(f"[主循环] retry_box = {retry_box}")
            if retry_box is not None:
                self.info_set("状态", "检测到重新挑战，点击")
                self.click_box(retry_box)
                self.sleep(2)

                box = None
                for i in range(60):
                    if global_state.stop_flag:
                        return
                    box = self.find_one(template=tpl, threshold=0.4)
                    self.log_info(f"[重挑后等炮塔] tpl_box = {box}")
                    if box is not None:
                        break
                    self.sleep(0.5)

                if box is not None:
                    cx = box.x + box.width // 2
                    cy = box.y + box.height // 2
                    rx = cx + random.randint(-10, 10)
                    ry = cy + random.randint(-10, 10)
                    self.swipe(rx, ry, 112, 835, duration=0.5)
                    self.sleep(1)

                    tpl_box = self.find_one(template=tpl, threshold=0.4)
                    if tpl_box is not None:
                        tx = tpl_box.x + tpl_box.width // 2
                        ty = tpl_box.y + tpl_box.height // 2
                        self.swipe(tx, ty, 367, 835, duration=0.5)
                        self.sleep(1)
                        tpl_box = self.find_one(template=tpl, threshold=0.4)
                        if tpl_box is not None:
                            tx = tpl_box.x + tpl_box.width // 2
                            ty = tpl_box.y + tpl_box.height // 2
                            self.swipe(tx, ty, 112, 835, duration=0.5)
                    self.sleep(0.5)

                    current_window = 1
                    phase = 2
                continue

            tpl_box = self.find_one(template=tpl, threshold=0.4)
            if tpl_box is None:
                self.sleep(0.5)
                continue

            cx = tpl_box.x + tpl_box.width // 2
            cy = tpl_box.y + tpl_box.height // 2
            trx = cx + random.randint(-10, 10)
            try_ = cy + random.randint(-10, 10)

            if phase == 2:
                roi = frame[60:250, :]
                roi_resized = cv2.resize(roi, (434, 190))
                results = self.model.predict(roi_resized, conf=0.5, verbose=False)
                boxes = results[0].boxes

                if len(boxes) > 0:
                    xs = []
                    for b in boxes:
                        x1, y1, x2, y2 = b.xyxy[0].tolist()
                        xs.append((x1 + x2) / 2)
                    avg_x = sum(xs) / len(xs)
                    target = 3 if avg_x > 217 else 1
                else:
                    target = 1

                if current_window != target:
                    self.info_set("状态", f"阶段二：拖到{target}号窗")
                    self.swipe(trx, try_, [112, 250, 367][target-1], 835, duration=0.5)
                    current_window = target

                zero_box = self.find_one(
                    template=zero_tpl, threshold=0.7,
                    box=self.box_of_screen(0.15, 0.68, 0.35, 0.75, name="zero_area")
                )
                if zero_box is not None:
                    self.info_set("状态", "一号窗已打完，进入阶段三")
                    phase = 3

            elif phase == 3:
                ammo_roi = frame[400:500, :]
                hsv = cv2.cvtColor(ammo_roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, (20, 100, 100), (35, 255, 255))
                ratio = np.sum(mask > 0) / mask.size
                ammo_full = ratio > 0.1
                self.info_set("子弹占比", f"{ratio:.2f}")

                zero_a = self.find_one(
                    template=zero_tpl, threshold=0.7,
                    box=self.box_of_screen(220/436, 630/965, 285/436, 660/965)
                )
                zero_b = self.find_one(
                    template=zero_tpl, threshold=0.7,
                    box=self.box_of_screen(220/436, 665/965, 285/436, 700/965)
                )
                phase4_ready = (zero_a is not None) and (zero_b is not None)

                if phase4_ready:
                    self.info_set("状态", "二号窗已打完，进入阶段四")
                    phase = 4
                else:
                    target = 2 if ammo_full else 1

                    if current_window != target:
                        self.info_set("状态", f"阶段三：子弹{ratio:.2f}，拖到{target}号窗")
                        self.swipe(trx, try_, [112, 250, 367][target-1], 835, duration=0.5)
                        current_window = target

            elif phase == 4:
                if current_window != 1:
                    self.info_set("状态", "阶段四：一直在一号窗")
                    self.swipe(trx, try_, 112, 835, duration=0.5)
                    current_window = 1

            self.sleep(0.5)

            try:
                del frame
            except:
                pass
            try:
                del results
            except:
                pass
            try:
                del boxes
            except:
                pass
            gc.collect()