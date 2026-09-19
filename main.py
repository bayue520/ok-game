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

# ===== 资源路径：PyInstaller 单 exe =====
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS          # 打包后的资源解压目录
    EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR

# 让 ok-script 能找到 src/、模型文件等
os.chdir(BASE_DIR)

# ok-script 任务配置
OK_SCRIPT_TASK = "AutoBattle"
OK_SCRIPT_CONFIG = "src.config:config"

ok_process = None
running_flag = False


# ===================== 自动化线程 =====================
def auto_battle_logic():
    """在后台线程中运行 ok-script 任务（无 GUI 模式）"""
    global running_flag
    try:
        # 无界面模式下，直接用 ok 的 CLI 逻辑跑任务
        # 这里不启动子进程，而是直接调用 ok 的命令行入口
        from ok.cli import main as ok_cli_main
        # 模拟命令行参数：ok run_task AutoBattle --config src.config:config
        sys.argv = ["ok", "run_task", OK_SCRIPT_TASK, "--config", OK_SCRIPT_CONFIG]
        ok_cli_main()
    except Exception as e:
        print(f"自动化运行出错: {e}")
    finally:
        running_flag = False


def start_ok_script():
    global running_flag, ok_process
    if running_flag:
        return
    running_flag = True
    # 用 daemon 线程，关闭主窗口时自动退出
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


def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# ===================== 卡密窗口 =====================
def card_verify_window():
    win = ttkb.Window(title="激活", themename="flatly", size=(420, 340),
                       resizable=(False, False))
    center_window(win, 420, 340)

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

    def verify(event=None):
        card = card_input.get().strip()
        if not card:
            status_label.configure(text="请输入卡密", bootstyle="danger")
            return
        status_label.configure(text="正在验证...", bootstyle="warning")
        win.update()
        ok_ret, msg = kamit_verify_card(card)
        if ok_ret:
            win.destroy()
            open_main_window()
        else:
            status_label.configure(text=f"验证失败：{msg}", bootstyle="danger")
            card_input.delete(0, END)

    card_input.bind("<Return>", verify)
    ttkb.Button(frame, text="登 录", command=verify,
                bootstyle="success", width=30).pack(pady=10, ipady=4)

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