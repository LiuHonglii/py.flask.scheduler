# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext
import shutil
from pathlib import Path
from application.common import CustomError


@click.command('del-migrations')
@with_appcontext
def destroy_migrations():
    """删除版本迁移文件夹"""
    BASE_DIR = Path.cwd()
    # 拼接路径
    path = Path.joinpath(BASE_DIR, 'migrations')

    if path.exists():
        try:
            shutil.rmtree(path)
        except Exception as e:
            raise CustomError(f'删除数据表失败 {e}')

        print('删除迁移文件夹完成===>[migrations]')
    else:
        print('迁移文件夹不存在===>[migrations]')
