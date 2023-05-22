# -*- coding: utf-8 -*-
import multiprocessing
from gevent import monkey

monkey.patch_all()

gunicorn_log_file_path = '/tmp'

wsgi_app = 'wsgi:app'

# 避免定时任务重复执行
# 这样在启动 worker 进程之前，会先加载 app，然后再 fork 出子进程，这样就可以保证只有一个 scheduler 对象
preload_app = True

# 并行工作进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 4 if (multiprocessing.cpu_count() * 2 + 1) <= 6 else 6

debug = False

reload = True  # 自动重新加载

loglevel = 'info'

backlog = 2048

# 指定每个工作者的线程数
# threads = 2

# 转发为监听端口5600
# bind = '0.0.0.0:5800'

raw_env = ['FLASK_DEBUG=0']

# 设置守护进程,将进程交给supervisor管理
daemon = False

# 工作模式协程
worker_class = 'gevent'

# 设置最大并发量
worker_connections = 2000

timeout = 60

# 设置进程文件目录
pidfile = f'{gunicorn_log_file_path}/gunicorn.pid'
logfile = f'{gunicorn_log_file_path}/debug.log'

# 设置访问日志和错误信息日志路径
accesslog = f'{gunicorn_log_file_path}/gunicorn_access.log'
errorlog = f'{gunicorn_log_file_path}/gunicorn_error.log'
