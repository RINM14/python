import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk


def simulate_blue_screen():
    def on_escape(event):
        root.destroy()

    root = tk.Tk()
    root.config(cursor="none")
    root.title("蓝屏死机")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="#0078D7")

    root.bind("<Escape>", on_escape)  # 绑定 Esc 键退出

    # 显示悲伤的表情
    sad_face_label = tk.Label(root, text=":(", fg="white", bg="#0078D7", font=("Segoe UI", 160, "bold"))
    sad_face_label.pack(pady=(100, 0), anchor="w", padx=100)

    # 显示错误信息
    error_message = """你的电脑遇到问题，需要重新启动。
我们只收集某些错误信息，然后你可以重新启动。

100% 完成"""
    error_message_label = tk.Label(root, text=error_message, fg="white", bg="#0078D7", font=("Microsoft YaHei", 26),
                                   justify="left", anchor="nw")
    error_message_label.pack(padx=100, pady=(10, 0), anchor="w")

    # 创建一个容器来放置二维码和详细信息
    frame = tk.Frame(root, bg="#0078D7")
    frame.pack(padx=100, pady=(40, 0), anchor="w")

    # 显示二维码图像
    qr_code_url = "https://i.postimg.cc/RZxDT5S0/123.png"
    try:
        response = requests.get(qr_code_url)
        qr_code_image = Image.open(BytesIO(response.content))
        qr_code_image = qr_code_image.resize((200, 200))  # 调整图像大小
        qr_code_photo = ImageTk.PhotoImage(qr_code_image)

        qr_code_label = tk.Label(frame, image=qr_code_photo, bg="#0078D7")
        qr_code_label.image = qr_code_photo  # 保持对图像的引用
        qr_code_label.pack(side="left", padx=(0, 20))

    except Exception as e:
        print("二维码图像加载失败:", e)

    # 详细信息
    detailed_info = """有关此问题的详细信息和可能的解决方法，请访问 https://www.windows.com/stopcode

如果您向支持人员，请向他们提供以下信息：
停止代码：KERNEL_DATA_INPAGE_ERROR"""
    detailed_info_label = tk.Label(frame, text=detailed_info, fg="white", bg="#0078D7", font=("Microsoft YaHei", 18),
                                   justify="left", anchor="nw")
    detailed_info_label.pack(side="left")

    root.mainloop()
