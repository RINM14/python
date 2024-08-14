# system_monitor.py

import psutil


def get_cpu_usage():
    """
    获取当前CPU使用率

    :return: 返回CPU使用率的百分比
    """
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    """
    获取当前内存使用情况

    :return: 返回已使用内存和总内存，以字典形式返回
    """
    memory = psutil.virtual_memory()
    return {
        'total_memory': memory.total,
        'used_memory': memory.used,
        'percent': memory.percent
    }
