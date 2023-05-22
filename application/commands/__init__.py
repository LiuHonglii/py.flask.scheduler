# -*- coding: utf-8 -*-
from flask import Flask


def init_commands(app: Flask):
    """
    初始化
    """
    from .init_cli import init_command_cli
    init_command_cli(app)
