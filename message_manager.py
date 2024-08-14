import ctypes
import logging
import os
import random

# 配置日志
logging.basicConfig(level=logging.INFO)

def random_popup():
    try:
        messages = [
            "系统警告！",
            "您的电脑可能感染了病毒！",
            "内存不足，请关闭一些程序。",
            "检测到恶意软件，请立即扫描。"
        ]

        # 从列表中随机选择一条消息
        message = random.choice(messages)
        os.system(f'msg * "{message}"')
        ctypes.windll.user32.MessageBoxW(0, message, "警告", 0x00000010 | 0x00000040)
        logging.info(f"执行随机弹窗: {message}")
    except Exception as e:
        logging.error("随机弹窗出错: %s", e)
