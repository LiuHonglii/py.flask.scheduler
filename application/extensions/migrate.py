# -*- coding: utf-8 -*-
from flask_migrate import Migrate

migrate = Migrate(render_as_batch=True, compare_type=True, compare_server_default=True)
