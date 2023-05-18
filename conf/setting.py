# -*- coding: utf-8 -*-
from application.exts.scheduler import SchedulerConfig


class Config(SchedulerConfig):
    # 日志配置
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024
    LOGGING_FILE_BACKUP = 10

    # json dumps 参数配置
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    # flask-sqlalchemy使用的参数
    # 默认数据库
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:postgres@127.0.0.1:5432/py.flask.scheduler'  # 数据库
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 7200
    SQLALCHEMY_MAX_OVERFLOW = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
    SQLALCHEMY_ECHO = False


config_dict = {
    'development': Config,
    # 'production': ProductionConfig,
    # 'testing': TestingConfig
}
