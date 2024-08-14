import os
import platform

def disconnect_network():
    """断开网络连接"""
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("ipconfig /release")
    elif system_platform == "Darwin" or system_platform == "Linux":
        os.system("sudo ifconfig eth0 down")
    else:
        print("不支持的操作系统")
