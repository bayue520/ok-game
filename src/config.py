import os

import numpy as np
from ok import ConfigOption

version = "dev"

app_profile = os.environ.get("PYAPPIFY_APP_PROFILE", "")
gui_config = {
    'type': 'web' if app_profile.casefold() == 'web' else 'qt',
    'window_size': {
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
}
if gui_config['type'] == 'web':
    gui_config['launch_mode'] = 'pywebview'

key_config_option = ConfigOption('Game Hotkey Config', {
    'Echo Key': 'q',
    'Liberation Key': 'r',
    'Resonance Key': 'e',
    'Tool Key': 't',
}, description='In Game Hotkey for Skills')

# ===== 新增：卡密配置 =====
card_config_option = ConfigOption('卡密', {
    'card': '',
}, description='请输入你的卡密')


def make_bottom_right_black(frame):
    try:
        height, width = frame.shape[:2]
        black_width = int(0.13 * width)
        black_height = int(0.025 * height)
        start_x = width - black_width
        start_y = height - black_height
        black_rect = np.zeros((black_height, black_width, frame.shape[2]), dtype=frame.dtype)
        frame[start_y:height, start_x:width] = black_rect
        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame

config = {
    'custom_tasks':True,
    'debug': False,
    'gui': gui_config,
    'config_folder': 'configs',
    'global_configs': [key_config_option, card_config_option],   # ← 加了 card_config_option
    'screenshot_processor': make_bottom_right_black,
    'gui_icon': 'icons/icon.png',
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0,
    'ocr': {
        'lib': 'onnxocr',
        'auto_simplify': True,
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {
        'interaction': ['Pynput', 'PostMessage', 'Genshin', 'PyDirect','ForegroundPostMessage'],
        'capture_method': ['WGC', 'BitBlt_RenderFull', 'BitBlt'],
        'check_hdr': False,
        'force_no_hdr': False,
        'require_bg': True
    },
    'adb': {
    },
    'browser': {
        'url': 'https://file.gugudang.com/res/down/public/p_yuanshiren/web-mobile/lts2/index.html?t=1772931238930',
        'nick': '生化地下城 让子弹射',
        'resolution': (434, 961),
    },
    'supported_resolution': {
        'ratio': '9:20',
        'min_size': (434, 961),
        'resize_to': [(434, 961)],
    },
    'links': {
            'default': {
                'github': 'https://github.com/ok-oldking/ok-script-app',
                'discord': 'https://discord.gg/vVyCatEBgA',
                'share': 'Download from https://github.com/ok-oldking/ok-script-app',
                'qq_group':'https://qm.qq.com/q/3Gq4VLvQe',
                'qq_channel': 'https://pd.qq.com/s/djmm6l44y',
                'faq': 'https://github.com/ok-oldking/ok-script-app'
            }
        },
    'screenshots_folder': "screenshots",
    'gui_title': '生化地下城 让子弹射',
    'template_matching': {
        'coco_feature_json': os.path.join('assets', 'coco_annotations.json'),
        'default_horizontal_variance': 0.002,
        'default_vertical_variance': 0.002,
        'default_threshold': 0.8,
    },
    'version': version,
    'my_app': ['src.globals', 'Globals'],
    'onetime_tasks': [
        ["src.tasks.MyOneTimeTask", "MyOneTimeTask"],
        ["ok", "DiagnosisTask"],
        ["src.tasks.AutoBattle", "AutoBattle"],
    ],
}