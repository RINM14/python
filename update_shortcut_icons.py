import ctypes
import logging
import os
from pathlib import Path
import requests
import win32com.client
import pythoncom

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 图标下载地址和路径
ICON_URL = "https://qntemp3.bejson.com/upload/16308358985970850.jpg?imageView2/1/w/64/h/64/format/ico/q/100&attname=202031421225810515.ico"
DESKTOP_PATH = Path(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
ICON_PATH = DESKTOP_PATH / 'icon.ico'

def update_shortcut_icon(shortcut_path, icon_path):
    """更新指定快捷方式的图标。"""
    try:
        pythoncom.CoInitialize()  # 初始化 COM 库

        logging.info(f"处理快捷方式: {shortcut_path}")
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.IconLocation = str(icon_path) + ", 0"
        shortcut.Save()
        logging.info(f"修改图标成功: {shortcut_path}")
    except Exception as e:
        logging.error(f"修改图标失败: {shortcut_path}, 错误: {e}")
    finally:
        pythoncom.CoUninitialize()  # 释放 COM 库

def update_all_desktop_shortcuts(icon_url=ICON_URL):
    """下载图标并更改所有桌面快捷方式的图标。"""
    try:
        # 下载图标
        response = requests.get(icon_url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(ICON_PATH, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"下载图标成功: {ICON_PATH}")

        # 更改所有桌面快捷方式图标
        for item in DESKTOP_PATH.glob('*.lnk'):
            update_shortcut_icon(item, ICON_PATH)

        logging.info("所有桌面快捷方式图标已更改")

        # 刷新桌面以显示更改
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, 0)
    except requests.RequestException as e:
        logging.error(f"下载图标失败: {e}")
    except Exception as e:
        logging.error(f"更改桌面快捷方式图标出错: {e}")

