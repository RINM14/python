import logging
import os
import random
import time

import psutil


# 获取当前进程的进程名
def get_current_process_name():
    return os.path.basename(os.path.abspath(__file__)).replace('.py', '.exe')


CURRENT_PROCESS_NAME = get_current_process_name()


def get_executable_files(drive):
    """
    遍历指定盘符的所有可执行文件路径
    """
    executable_files = []
    for root, dirs, files in os.walk(drive):
        for file in files:
            if file.endswith('.exe'):
                executable_files.append(os.path.join(root, file))
    return executable_files


def open_applications():
    """
    随机打开 C 盘和 D 盘上的一个应用程序
    """
    try:
        logging.info("启动自动打开应用程序")

        drives = ['C:', 'D:']
        for drive in drives:
            executable_files = get_executable_files(drive)
            executable_files = [file for file in executable_files if os.path.basename(file) != CURRENT_PROCESS_NAME]

            if executable_files:
                app = random.choice(executable_files)
                logging.info(f"尝试启动应用程序: {app}")
                try:
                    os.system(f"start \"{app}\"")
                    time.sleep(random.uniform(1, 5))  # 随机延迟 1 到 5 秒
                except Exception as e:
                    logging.error(f"启动应用程序失败: {app}, 错误: {e}")

    except Exception as e:
        logging.error("自动化打开应用程序出错: %s", e)


def close_applications():
    """
    随机关闭当前系统中所有可关闭的应用程序
    """
    try:
        logging.info("启动自动关闭应用程序")

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] != CURRENT_PROCESS_NAME:
                try:
                    logging.info(f"尝试关闭应用程序: {proc.info['name']}")
                    proc.terminate()  # 尝试终止进程
                    time.sleep(random.uniform(1, 5))  # 随机延迟 1 到 5 秒
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logging.error(f"关闭应用程序失败: {proc.info['name']}, 错误: {e}")

    except Exception as e:
        logging.error("自动化关闭应用程序出错: %s", e)


def main(action):
    if action == "open":
        open_applications()
    elif action == "close":
        close_applications()
    else:
        logging.error("无效的操作选项: %s", action)


# 初始化日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
