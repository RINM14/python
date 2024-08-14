import time
import ctypes

def apply_mouse_click_delay(delay_seconds=2):
    """延迟鼠标点击操作"""
    time.sleep(delay_seconds)
    ctypes.windll.user32.BlockInput(True)  # 阻止鼠标输入
    time.sleep(delay_seconds)  # 延迟指定时间
    ctypes.windll.user32.BlockInput(False)  # 解除鼠标输入阻止

