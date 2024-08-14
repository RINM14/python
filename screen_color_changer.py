import tkinter as tk
import random
import time
import threading


def change_color():
    # 随机生成颜色
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def start_color_change():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg=change_color())

    def update_color():
        while True:
            time.sleep(10)  # 等待10秒
            root.configure(bg=change_color())

    # 启动一个线程以防止阻塞界面
    threading.Thread(target=update_color, daemon=True).start()

    root.mainloop()


