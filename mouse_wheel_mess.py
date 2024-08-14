import ctypes
import random
import time

def apply_mouse_wheel_mess(duration_seconds=10):
    """随机滚动鼠标滚轮"""
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        scroll_amount = random.randint(-120, 120)  # 随机滚动量
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, scroll_amount, 0)  # 滚动鼠标滚轮
        time.sleep(0.1)  # 控制滚动速度

