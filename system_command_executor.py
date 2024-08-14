import logging
import random
import subprocess
import os
import time

def open_system_settings():
    try:
        logging.info("启动随机弹出系统设置窗口")
        settings = ["ms-settings:display", "ms-settings:appsfeatures", "ms-settings:windowsupdate"]
        while True:
            setting = random.choice(settings)
            os.system(f"start {setting}")
            time.sleep(random.randint(30, 60))
    except Exception as e:
        logging.error("随机弹出系统设置窗口出错: %s", e)

def text_conversion():
    try:
        logging.info("执行文字转化")
        text = "这是需要转化的文字"
        conversion_map = {char: chr((ord(char) + 3) % 256) for char in text}
        converted_text = ''.join(conversion_map.get(char, char) for char in text)
        logging.info('转化后的文字: ' + converted_text)
    except Exception as e:
        logging.error("文字转化出错: %s", e)

def system_reboot_or_shutdown():
    """
    随机选择执行系统重启或关机命令，概率为 50/50。
    """
    try:
        logging.info("启动自动重启和关机")

        probability = random.random()
        if probability < 0.5:  # 50% 的概率执行重启
            logging.info("50% 概率触发：系统即将重启")
            subprocess.run("shutdown /r /t 0", shell=True, check=True)  # 立即重启
        else:  # 50% 的概率执行关机
            logging.info("50% 概率触发：系统即将关机")
            subprocess.run("shutdown /s /t 0", shell=True, check=True)  # 立即关机

    except Exception as e:
        logging.error("自动重启和关机出错: %s", e)

# 初始化日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
