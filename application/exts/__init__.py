# -*- coding: utf-8 -*-
from flask import Flask
from .scheduler import custom_scheduler


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
    custom_scheduler.init_app(app)