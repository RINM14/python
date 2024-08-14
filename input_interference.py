import logging
import random
import time
import keyboard
import pyautogui

# 配置日志
logging.basicConfig(level=logging.INFO)

def mouse_interference():
    try:
        logging.info("启动鼠标干扰")
        screen_width, screen_height = pyautogui.size()
        while True:
            # 随机生成鼠标目标位置
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            # 移动鼠标到随机位置
            pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))  # 持续时间在0.5到1.5秒之间
            time.sleep(random.randint(5, 15))  # 随机等待时间
    except Exception as e:
        logging.error("鼠标干扰出错: %s", e)
def keyboard_interference():
    # 定义所有标准 108 键按键
    keys = [
        'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
        'print screen', 'scroll lock', 'pause', 'tilde', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '-', '=', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
        'caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter',
        'left shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift',
        'left ctrl', 'left win', 'left alt', 'space', 'right alt', 'right win', 'apps', 'right ctrl',
        'insert', 'home', 'page up', 'delete', 'end', 'page down', 'left', 'up', 'right', 'down',
        'num lock', '/', '*', '-', '7', '8', '9',
        '+', '4', '5', '6', '1', '2', '3',
        '0', '.'
    ]

    # 定义需要特殊处理的功能键
    modifier_keys = [
        'left shift', 'right shift', 'left ctrl', 'right ctrl',
        'left alt', 'right alt', 'left win', 'right win',
        'caps lock', 'num lock', 'scroll lock'
    ]

    # 存储按下的键及其映射，以确保对应释放
    pressed_keys = {}

    def map_key_event(event):
        if event.event_type == 'down':
            if event.name not in modifier_keys:
                # 随机映射一个按键
                mapped_key = random.choice(keys)
                pressed_keys[event.name] = mapped_key
                keyboard.press(mapped_key)
            else:
                # 直接传递功能键的按下事件
                keyboard.press(event.name)
        elif event.event_type == 'up':
            mapped_key = pressed_keys.get(event.name)
            if mapped_key:
                keyboard.release(mapped_key)
                del pressed_keys[event.name]
            else:
                # 直接传递功能键的释放事件
                keyboard.release(event.name)

    # 设置键盘监听
    keyboard.hook(map_key_event)
    logging.info("键盘干扰已启动")

    # 在干扰期间，随机休眠一段时间，避免持续干扰
    try:
        while True:
            time.sleep(random.uniform(1, 5))
    except KeyboardInterrupt:
        logging.info("键盘干扰已终止")
