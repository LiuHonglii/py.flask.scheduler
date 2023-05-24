# -*- coding: utf-8 -*-
from flask import Flask


def init_command_cli(app: Flask):
    """注册命令行工具"""

    # 数据初始化
    from .init_db_cli import init_db
    app.cli.add_command(init_db)

    # 版本控制表删除
    from .destroy_alembic_version_cli import destroy_alembic_version
    app.cli.add_command(destroy_alembic_version)

    # 迁移文件删除
    from .destroy_migrations_cli import destroy_migrations
    app.cli.add_command(destroy_migrations)
