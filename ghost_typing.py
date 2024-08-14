import logging
import random
import time

import pyautogui

# 定义随机内容的列表，并添加更多内容
CONTENT_LIST = [
    "请忽略这条信息",
    "注意：此消息由系统自动生成",
    "检查您的系统设置",
    "这是一个测试消息",
    "系统出现异常，请重启计算机",
    "警告：系统未响应",
    "请插入恢复光盘",
    "更新您的软件以避免问题",
    "系统即将关闭",
    "内存不足，请关闭一些应用程序",
    "未知错误已发生",
    "错误代码: 0x80070057",
    "设备驱动程序不兼容",
    "磁盘空间不足",
    "请立即保存您的工作"
]

def ghost_typing():
    try:
        logging.info("启动幽灵输入")
        while True:
            # 随机选择内容
            content = random.choice(CONTENT_LIST)
            pyautogui.typewrite(content)
            #time.sleep(random.randint(10, 20))  # 随机等待时间
    except Exception as e:
        logging.error("幽灵输入出错: %s", e)
        # 重新启动幽灵输入以提高稳定性
        #time.sleep(5)  # 延迟后重新启动
        ghost_typing()  # 重新启动功能