import configparser
import os

# 初始化配置解析器
config = configparser.ConfigParser()

# 默认配置
DEFAULT_CONFIG = {
    'server': {
        'ip': '192.168.10.45',
        'port': '5002'
    },
    'retry': {
        'interval': '5'
    },
    'heartbeat': {
        'interval': '10'
    },
    'Settings': {
        'monitor_timeout': '60'
    }
}

# 获取配置文件路径
def get_config_paths():
    """
    获取可能的配置文件路径列表，并优先读取其中一个
    """
    app_data_path = os.path.join('C:\\', 'AppData', 'Roaming', '.ecloud')
    current_dir_path = 'config.ini'
    return [os.path.join(app_data_path, 'config.ini'), current_dir_path]

# 读取配置文件
def load_config():
    """
    加载指定的配置文件。如果文件不存在，则在所有指定路径下创建一个包含默认值的配置文件。
    """
    config_files = get_config_paths()
    found = False
    for config_file in config_files:
        if os.path.exists(config_file):
            config.read(config_file)
            found = True
            break

    # 如果所有配置文件都不存在，则创建默认配置文件在所有路径下
    if not found:
        for config_file in config_files:
            create_default_config(config_file)

def create_default_config(config_file):
    """
    创建一个包含默认值的配置文件
    """
    for section, options in DEFAULT_CONFIG.items():
        config.add_section(section)
        for key, value in options.items():
            config.set(section, key, value)

    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# 获取服务器 IP
def get_server_ip():
    """
    从配置文件中获取服务器 IP 地址
    """
    return config.get('server', 'ip')

# 获取服务器端口
def get_server_port():
    """
    从配置文件中获取服务器端口号
    """
    return config.getint('server', 'port')

# 获取重试间隔时间
def get_retry_interval():
    """
    从配置文件中获取重试间隔时间
    """
    try:
        return config.getint('retry', 'interval')
    except ValueError as e:
        raise ValueError(f"配置文件中的重试间隔时间无效: {e}")

# 获取心跳间隔时间
def get_heartbeat_interval():
    """
    从配置文件中获取心跳间隔时间
    """
    try:
        return config.getint('heartbeat', 'interval')
    except ValueError as e:
        raise ValueError(f"配置文件中的心跳间隔时间无效: {e}")

# 获取监控超时时间
def get_monitor_timeout():
    """
    从配置文件中获取监控超时时间
    """
    try:
        return config.getint('Settings', 'monitor_timeout')
    except ValueError as e:
        raise ValueError(f"配置文件中的监控超时时间无效: {e}")

# 调用 load_config() 加载配置
load_config()
