# registry_manager.py

import winreg


def read_registry_value(key, subkey, value_name):
    """
    读取注册表键值

    :param key: 根键（如 HKEY_LOCAL_MACHINE）
    :param subkey: 子键路径
    :param value_name: 键值名称
    :return: 返回读取到的键值数据，如果失败返回 None
    """
    try:
        registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, value_name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


def write_registry_value(key, subkey, value_name, value, value_type):
    """
    写入注册表键值

    :param key: 根键（如 HKEY_LOCAL_MACHINE）
    :param subkey: 子键路径
    :param value_name: 键值名称
    :param value: 要写入的值
    :param value_type: 值的类型（如 winreg.REG_SZ 表示字符串类型）
    :return: 如果写入成功返回 True，否则返回 False
    """
    try:
        registry_key = winreg.CreateKey(key, subkey)
        winreg.SetValueEx(registry_key, value_name, 0, value_type, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def delete_registry_value(key, subkey, value_name):
    """
    删除注册表键值

    :param key: 根键（如 HKEY_LOCAL_MACHINE）
    :param subkey: 子键路径
    :param value_name: 键值名称
    :return: 如果删除成功返回 True，否则返回 False
    """
    try:
        registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(registry_key, value_name)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False
