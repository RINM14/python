# task_scheduler.py

import time

import schedule


def job():
    """
    定时任务的具体功能

    :return: 无
    """
    print("任务正在执行...")


def schedule_task(interval, unit, task):
    """
    调度任务

    :param interval: 时间间隔（数字）
    :param unit: 时间单位（如 'seconds', 'minutes', 'hours'）
    :param task: 要执行的任务函数
    :return: 无
    """
    if unit == 'seconds':
        schedule.every(interval).seconds.do(task)
    elif unit == 'minutes':
        schedule.every(interval).minutes.do(task)
    elif unit == 'hours':
        schedule.every(interval).hours.do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
