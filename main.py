import tkinter as tk
from tkinter import messagebox
import sys
import os
import uuid
import time
import datetime
import urllib.request
import urllib.parse
import ssl
import base64
import threading

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# ===== 卡密通配置 =====
USER_ID = "xiaoyin1110"
APP_NAME = "shenghuadixiachengduobizidan"
PRIMARY_DOMAIN = base64.b64decode("d3d3LmtleXQuY24=").decode("utf-8")


# ===== 资源路径：打包后代码和资源都在 exe 同级的 my/ 文件夹 =====
if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))
    BASE_DIR = os.path.join(EXE_DIR, "my")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR

os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# ===== 卡密保存文件 =====
CARD_FILE = os.path.join(EXE_DIR, "card.txt")

running_flag = False
ok_instance = None


# ===================== 自动化线程 =====================
def auto_battle_logic():
    global running_flag, ok_instance
    try:
        from ok import OK
        from src.config import config
        from src.tasks.AutoBattle import AutoBattle

        headless_config = dict(config)
        headless_config.pop("gui", None)
        headless_config["use_gui"] = False
        headless_config["check_mutex"] = False

        print(">>> create OK instance")
        ok_instance = OK(headless_config)

        print(">>> calling OK.run_task")
        ok_instance.run_task(AutoBattle, exit_after=False)
    except Exception as e:
        import traceback
        print(f"自动化运行出错: {e}")
        traceback.print_exc()
    finally:
        running_flag = False


def start_ok_script():
    global running_flag
    if running_flag:
        return
    running_flag = True
    t = threading.Thread(target=auto_battle_logic, daemon=True)
    t.start()


def stop_ok_script():
    global running_flag
    running_flag = False


# ===================== 卡密验证 =====================
def get_machine_code():
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        return mac + "MAC"
    except:
        return "FFFFFFFFFFFFMAC"


def kamit_verify_card(card):
    mac = get_machine_code()
    t = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = f"/kami/{USER_ID}/check.php"
    params = {
        "card": card, "mac": mac, "app": APP_NAME, "t": t,
        "_t": int(time.time())
    }
    full_url = f"https://{PRIMARY_DOMAIN}{path}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(full_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=15, context=context) as resp:
            data = resp.read().decode('utf-8')
        if "ok|" in data or "bypass" in data:
            return True, "验证成功"
        elif "error|" in data:
            return False, data.split("|")[1]
        else:
            return False, data
    except Exception as e:
        return False, f"网络连接失败: {e}"


def translate_error(msg):
    m = msg.lower()
    if "<!doctype" in m or "<html" in m:
        return "服务器返回异常，请检查网络或稍后重试"
    if "invalid_card" in m or "not_found" in m or "not found" in m or "invalid" in m:
        return "卡密不存在或已失效"
    if "too_frequent" in m or "too frequent" in m:
        return "请求太频繁，请 50 秒后再试"
    if "expired" in m or "timeout" in m or "out of date" in m:
        return "卡密已过期"
    if "used" in m:
        return "卡密已被使用"
    if "mac" in m or "bind" in m:
        return "卡密已绑定到其他设备"
    if "network" in m or "连接" in msg:
        return f"网络连接失败：{msg}"
    return f"验证失败：{msg}"


def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# ===================== 卡密窗口 =====================
def card_verify_window():
    win = ttkb.Window(title="激活", themename="flatly", size=(420, 420),
                       resizable=(False, False))
    center_window(win, 420, 420)

    frame = ttkb.Frame(win, padding=40)
    frame.pack(fill=BOTH, expand=YES)

    ttkb.Label(frame, text="🎮", font=("Segoe UI Emoji", 36)).pack(pady=(0, 10))
    ttkb.Label(frame, text="闪语-骰子地下城-躲避子弹5",
               font=("微软雅黑", 14, "bold")).pack()
    ttkb.Label(frame, text="请输入激活卡密", font=("微软雅黑", 10),
               bootstyle="secondary").pack(pady=(8, 20))

    card_input = ttkb.Entry(frame, font=("微软雅黑", 12), width=30)
    card_input.pack(pady=6, ipady=6)
    card_input.focus()

    status_label = ttkb.Label(frame, text="", font=("微软雅黑", 9))
    status_label.pack(pady=(2, 10))

    def do_verify(card, remember=True):
        status_label.configure(text="正在验证...", bootstyle="warning")
        win.update()
        ok_ret, msg = kamit_verify_card(card)
        if ok_ret:
            if remember:
                try:
                    with open(CARD_FILE, "w", encoding="utf-8") as f:
                        f.write(card)
                except Exception:
                    pass
            win.destroy()
            open_main_window()
        else:
            status_label.configure(text=translate_error(msg), bootstyle="danger")
            card_input.delete(0, END)

    def verify(event=None):
        card = card_input.get().strip()
        if not card:
            status_label.configure(text="请输入卡密", bootstyle="danger")
            return
        do_verify(card, remember=True)

    card_input.bind("<Return>", verify)
    ttkb.Button(frame, text="登 录", command=verify,
                bootstyle="success", width=30).pack(pady=10, ipady=4)

    def auto_login():
        if os.path.exists(CARD_FILE):
            try:
                with open(CARD_FILE, "r", encoding="utf-8") as f:
                    saved = f.read().strip()
                if saved:
                    card_input.delete(0, tk.END)
                    card_input.insert(0, saved)
            except Exception:
                pass

    win.after(300, auto_login)
    win.mainloop()


# ===================== 主界面 =====================
def open_main_window():
    win = ttkb.Window(title="自动战斗", themename="flatly",
                       size=(420, 320), resizable=(False, False))
    center_window(win, 420, 320)

    frame = ttkb.Frame(win, padding=30)
    frame.pack(fill=BOTH, expand=YES)

    ttkb.Label(frame, text="闪语-骰子地下城-躲避子弹5",
               font=("微软雅黑", 14, "bold")).pack(pady=(0, 5))

    status_var = tk.StringVar(value="● 未启动")
    status_label = ttkb.Label(frame, textvariable=status_var,
                               font=("微软雅黑", 11), bootstyle="secondary")
    status_label.pack(pady=10)

    btn_frame = ttkb.Frame(frame)
    btn_frame.pack(pady=20)

    def start_script():
        start_ok_script()
        status_var.set("● 运行中")
        status_label.configure(bootstyle="success")

    def stop_script():
        stop_ok_script()
        status_var.set("● 已停止")
        status_label.configure(bootstyle="danger")
        try:
            win.quit()
        except Exception:
            pass
        try:
            win.destroy()
        except Exception:
            pass
        sys.exit(0)

    ttkb.Button(btn_frame, text="▶  开始", command=start_script,
                bootstyle="success", width=12).grid(row=0, column=0, padx=10, ipady=8)
    ttkb.Button(btn_frame, text="■  停止", command=stop_script,
                bootstyle="danger", width=12).grid(row=0, column=1, padx=10, ipady=8)

    def on_close():
        stop_ok_script()
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_close)

    win.mainloop()


if __name__ == "__main__":
    card_verify_window()