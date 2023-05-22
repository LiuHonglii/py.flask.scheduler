# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext
from application.commands.initialize import Initialize


@click.command('del-alembic-version')
@with_appcontext
def destroy_alembic_version():
    """删除版本库控制表"""
    Initialize().destroy_alembic_version()
