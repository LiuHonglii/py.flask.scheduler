# -*- coding: utf-8 -*-
import atexit
import platform
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
import click


# 定时器配置项
class SchedulerConfig():
    # 线程池配置，最大20个线程
    SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
    # 持久化存储
    SCHEDULER_SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@172.16.80.121:5432/py.flask.scheduler'
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SCHEDULER_SQLALCHEMY_DATABASE_URI)}
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
        # 启动定时任务服务
        self.start()
        click.echo(' * Scheduler Started ---------------')

    def _load_lock(self):
        """
        文件锁形式 防止创建多个apscheduler任务实例
        存在问题：导致无法动态添加或变更任务
        :return:
        """
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
                # from application.scheduler import monitor
                # from application.scheduler import jobs
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
