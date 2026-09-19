import uuid
import time
import datetime
import urllib.request
import urllib.parse
import ssl
import base64
from ok import BaseTask


USER_ID = "xiaoyin1110"
APP_NAME = "shenghuadixiachengduobizidan"
PRIMARY_DOMAIN = base64.b64decode("d3d3LmtleXQuY24=").decode("utf-8")


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
        "card": card,
        "mac": mac,
        "app": APP_NAME,
        "t": t,
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
            err = data.split("|")[1]
            return False, err
        else:
            return False, data
    except Exception as e:
        return False, f"网络连接失败: {e}"


class LoginTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "LoginTask"
        self.description = "卡密验证"

        self.default_config.update({
            "卡密": "",
        })

    def run(self):
        card = self.config.get("卡密", "").strip()

        if not card:
            self.info_set("状态", "请输入卡密")
            return

        self.info_set("状态", "正在验证...")
        ok, msg = kamit_verify_card(card)

        if ok:
            self.info_set("状态", "验证成功")
            self.log_info("卡密验证成功")
        else:
            self.info_set("状态", f"验证失败：{msg}")
            self.log_info(f"卡密验证失败：{msg}")