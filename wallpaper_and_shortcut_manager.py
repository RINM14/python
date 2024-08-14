import ctypes
import logging
import os
import random
import time
import winreg
import requests

# 壁纸下载函数
def download_wallpaper(url, filename):
    """从指定的 URL 下载壁纸并保存到指定的文件。"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"下载壁纸成功: {filename}")
    except requests.RequestException as e:
        logging.error(f"下载壁纸失败: {e}")

# 壁纸 URL 配置
WALLPAPER_URLS = {
    "wallpaper1": "https://img1.baidu.com/it/u=439550839,3329274289&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=888",
    "wallpaper2": "https://img1.baidu.com/it/u=1321829697,3287464521&fm=253&fmt=auto&app=138&f=JPEG",
    "wallpaper3": "https://img0.baidu.com/it/u=2397665193,3930796322&fm=253&fmt=auto&app=138&f=JPEG"
}

# 更换壁纸函数
def change_wallpaper():
    """下载壁纸并定期更换壁纸。"""
    try:
        logging.info("启动更改壁纸")
        temp_dir = os.path.join(os.getenv('TEMP'), 'wallpapers')
        os.makedirs(temp_dir, exist_ok=True)

        wallpapers = list(WALLPAPER_URLS.keys())
        wallpaper_files = [os.path.join(temp_dir, f"{name}.jpg") for name in wallpapers]

        # 下载壁纸
        for name, url in WALLPAPER_URLS.items():
            file_path = os.path.join(temp_dir, f"{name}.jpg")
            if not os.path.exists(file_path):
                download_wallpaper(url, file_path)

        # 设置壁纸显示方式为居中
        set_wallpaper_style("center")

        while True:
            wallpaper = os.path.abspath(random.choice(wallpaper_files))
            if os.path.exists(wallpaper):
                logging.info(f"更换壁纸: {wallpaper}")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 3)
            else:
                logging.warning(f"壁纸文件不存在: {wallpaper}")
            time.sleep(random.randint(60, 300))
    except Exception as e:
        logging.error("更改壁纸出错: %s", e)

# 设置壁纸样式函数
def set_wallpaper_style(style):
    """根据给定的样式设置壁纸样式（居中、拉伸、填充、适合、平铺）。"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
        if style == "center":
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == "stretch":
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == "fill":
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == "fit":
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "6")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == "tile":
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
        key.Close()
        logging.info(f"壁纸样式设置为: {style}")
    except Exception as e:
        logging.error("设置壁纸样式出错: %s", e)
