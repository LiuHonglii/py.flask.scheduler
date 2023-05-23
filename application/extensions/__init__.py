# -*- coding: utf-8 -*-
from .app import Flask


def init_ext(app: Flask):
    """
    初始化扩展
    :param app:
    :return:
    """
    # 数据库初始化
    from ..models import db
    db.init_app(app)

    # migrate 初始化
    from .migrate import migrate
    migrate.init_app(app, db)

    # 跨域初始化
    from .cors import cors
    cors.init_app(app)

    # 定时任务初始化
    from .scheduler import custom_scheduler
    custom_scheduler.init_app(app)
