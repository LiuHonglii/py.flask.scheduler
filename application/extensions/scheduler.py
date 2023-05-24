# -*- coding: utf-8 -*-
import atexit
import os
import platform
import socket
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
import click
from blinker import signal


# 定时器配置项
class SchedulerConfig():
    # 线程池配置，最大20个线程
    SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
    # 持久化存储
    SCHEDULER_SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'postgresql://postgres:postgres@127.0.0.1:5432/py.flask.scheduler'
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url=SCHEDULER_SQLALCHEMY_DATABASE_URI)
    }
    # 配置允许执行定时任务的主机名
    SCHEDULER_ALLOWED_HOSTS = ['*']
    # 调度开关开启
    SCHEDULER_API_ENABLED = True
    # 设置容错时间为 1小时
    SCHEDULER_JOB_DEFAULTS = {'coalesce': True, 'max_instances': 3, 'misfire_grace_time': 60}
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

    # 序列化输出样式
    JSONIFY_PRETTYPRINT_REGULAR = True

    SCHEDULER_JOBS = [
        {
            "id": "id_get_all_jobs",
            "name": "获取所有任务",
            "func": "application:scheduler.jobs.get_all_jobs",
            "trigger": "interval",
            "seconds": 10,
            "replace_existing": True
        },
        {
            "id": "id_get_current_datetime",
            "name": "获取当前时间",
            "func": "application:scheduler.jobs.get_current_datetime",
            "trigger": "interval",
            "kwargs": {
                "name": "用户名称"
            },
            "seconds": 5,
            "replace_existing": True
        },
        {
            "id": "id_get_summation",
            "name": "求和",
            "func": "application:scheduler.jobs.get_summation",
            "trigger": "interval",
            "args": [
                4,
                5
            ],
            "seconds": 20,
            "replace_existing": True
        }
    ]


class CustomAPScheduler(APScheduler):

    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)

    def init_app(self, app):
        """
        :param app:
        :return:
        """
        super(CustomAPScheduler, self).init_app(app)
        from application.scheduler import monitor  # noqa: F401

        # 方式一
        self._socket_lock()
        # 方式二
        # self._load_lock()

    def init_start(self):
        """启动定时任务服务"""
        self.start(paused=True)
        click.echo(' * Scheduler Started ---------------')

    def _socket_lock(self):
        """
        借助套接字限制启动数量 会占用掉一个端口
        在init_app中调用
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 47200))
        except socket.error:
            pass
        else:
            self.init_start()

    def _load_lock(self):
        """
        文件锁形式 防止创建多个apscheduler任务实例
        存在问题：导致无法动态添加或变更任务
        在init_app中调用
        :return:
        """
        if platform.system() != 'Windows':
            # Linux 环境下
            fcntl = __import__("fcntl")
            f = open('./aps.lock', 'wb')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.init_start()
            except:
                pass

            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()

            atexit.register(unlock)
        else:
            # Window 环境下
            msvcrt = __import__('msvcrt')
            f = open('scheduler.lock', 'wb')
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                self.init_start()
            except:
                pass

            def _unlock_file():
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass

            atexit.register(_unlock_file)

    def _resume_signal(self, sender, **kwargs):
        """任务恢复信号"""
        self.resume()


custom_scheduler = CustomAPScheduler()

# 任务恢复信号
resume_signal = signal("resume_signal")

resume_signal.connect(custom_scheduler._resume_signal)
