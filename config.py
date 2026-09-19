import os

import numpy as np
from ok import ConfigOption

version = "dev"
#不需要修改version, Github Action打包会自动修改

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

key_config_option = ConfigOption('Game Hotkey Config', { #全局配置示例
    'Echo Key': 'q',
    'Liberation Key': 'r',
    'Resonance Key': 'e',
    'Tool Key': 't',
}, description='In Game Hotkey for Skills')


def make_bottom_right_black(frame): #可选. 某些游戏截图时遮挡UID使用
    """
    Changes a portion of the frame's pixels at the bottom right to black.

    Args:
        frame: The input frame (NumPy array) from OpenCV.

    Returns:
        The modified frame with the bottom-right corner blackened.  Returns the original frame
        if there's an error (e.g., invalid frame).
    """
    try:
        height, width = frame.shape[:2]  # Get height and width

        # Calculate the size of the black rectangle
        black_width = int(0.13 * width)
        black_height = int(0.025 * height)

        # Calculate the starting coordinates of the rectangle
        start_x = width - black_width
        start_y = height - black_height

        # Create a black rectangle (NumPy array of zeros)
        black_rect = np.zeros((black_height, black_width, frame.shape[2]), dtype=frame.dtype)  # Ensure same dtype

        # Replace the bottom-right portion of the frame with the black rectangle
        frame[start_y:height, start_x:width] = black_rect

        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame

config = {
    'custom_tasks':True, # enable creating and editing custom tasks
    'debug': False,  # Optional, default: False
    'gui': gui_config,
    'config_folder': 'configs', #最好不要修改
    'global_configs': [key_config_option],
    'screenshot_processor': make_bottom_right_black, # 在截图的时候对frame进行修改, 可选
    'gui_icon': 'icons/icon.png', #窗口图标, 最好不需要修改文件名
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0,
    'ocr': { #可选, 使用的OCR库
        'lib': 'onnxocr',
        'auto_simplify': True,
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {  # Windows游戏请填写此设置
        'interaction': ['Pynput', 'PostMessage', 'Genshin', 'PyDirect','ForegroundPostMessage'],
        'capture_method': ['WGC', 'BitBlt_RenderFull', 'BitBlt'],
        'check_hdr': False,
        'force_no_hdr': False,
        'require_bg': True
    },
    'adb': {  # 模拟器或Android设备请填写此设置
    },
    'browser': {
        'url': 'https://file.gugudang.com/res/down/public/p_yuanshiren/web-mobile/lts2/index.html?t=1772931238930',
        'nick': '生化地下城 让子弹射',
        'resolution': (434, 961),
    },
    'start_timeout': 120,  # default 60
    'supported_resolution': {
        'ratio': '9:20',
        'min_size': (434, 961),
        'resize_to': [(434, 961)],
    },
    'links': { # 关于里显示的链接, 可选
            'default': {
                'github': 'https://github.com/ok-oldking/ok-script-app',
                'discord': 'https://discord.gg/vVyCatEBgA',
                'share': 'Download from https://github.com/ok-oldking/ok-script-app',
                'qq_group':'https://qm.qq.com/q/3Gq4VLvQe',
                'qq_channel': 'https://pd.qq.com/s/djmm6l44y',
                'faq': 'https://github.com/ok-oldking/ok-script-app'
            }
        },
    'screenshots_folder': "screenshots", #截图存放目录, 每次重新启动会清空目录
    'gui_title': '生化地下城 让子弹射',  #窗口名
    'template_matching': { # 可选, 如使用OpenCV的模板匹配
        'coco_feature_json': os.path.join('assets', 'coco_annotations.json'),
        'default_horizontal_variance': 0.002,
        'default_vertical_variance': 0.002,
        'default_threshold': 0.8,
    },
    'version': version, #版本
    'my_app': ['src.globals', 'Globals'], #可选. 全局单例对象, 可以存放加载的模型, 使用og.my_app调用
    'onetime_tasks': [  # 用户点击触发的任务
        ["src.tasks.MyOneTimeTask", "MyOneTimeTask"],
        ["ok", "DiagnosisTask"],
        ["src.tasks.TestDrag", "TestDrag"],
    ],
}