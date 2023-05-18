# -*- coding: utf-8 -*-
import atexit
import platform
from flask_apscheduler import APScheduler


# 定时器配置项
class SchedulerConfig():
    # 线程池配置，最大20个线程
    SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
    # 配置允许执行定时任务的主机名
    SCHEDULER_ALLOWED_HOSTS = ['*']
    # 调度开关开启
    SCHEDULER_API_ENABLED = True
    # 设置容错时间为 1小时
    SCHEDULER_JOB_DEFAULTS = {'coalesce': True, 'max_instances': 3, 'misfire_grace_time': 60}
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

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

        if platform.system() != 'Windows':
            # Linux 环境下
            fcntl = __import__("fcntl")
            f = open('./aps.lock', 'wb')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.start()
                print(' * Scheduler Started,---------------')
                from application.scheduler import monitor
                from application.scheduler import jobs
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
                self.start()
                print(' * Scheduler Started In Window,---------------')
                from application.scheduler import monitor
                from application.scheduler import jobs
            except:
                pass

            def _unlock_file():
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass

            atexit.register(_unlock_file)

custom_scheduler = CustomAPScheduler()
