# -*- coding: utf-8 -*-
import os
from pathlib import Path
from .extensions import Flask
from conf.setting import config_dict
from application.views import register_blueprint
from .extensions.scheduler import resume_signal


def create_app():
    """
    创建Flask应用
    :return: app
    """

    BASE_DIR = Path(__file__).parent.parent
    app = Flask('py.flask.scheduler', root_path=f'{BASE_DIR}')

    config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config_dict[config_name])

    from .common import init_common
    init_common(app)

    # 命令行命令添加
    from .commands import init_commands
    init_commands(app)

    # 扩展初始化
    from .extensions import init_ext
    init_ext(app)

    # 注册蓝图
    register_blueprint(app)

    # 任务恢复信号
    resume_signal.send(app)

    return app
