# -*- coding: utf-8 -*-
from flask import Flask
from .logging import create_logger
from .response import success_resp
from .response import error_resp
from .exceptions import CustomError


def init_common(app: Flask):
    """
    初始化
    """
    # 配置日志
    create_logger(app)

    # 设置全局异常处理
    app.register_error_handler(Exception, CustomError._error_handler)
