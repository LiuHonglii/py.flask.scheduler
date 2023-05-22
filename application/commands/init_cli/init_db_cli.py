# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext
from application.commands.initialize import Initialize


@click.command('init-db')
@with_appcontext
def init_db():
    """初始化项目数据"""
    Initialize().run()
