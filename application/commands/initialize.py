# -*- coding: utf-8 -*-
from pathlib import Path
from .core_initialize import CoreInitialize

BASE_DIR = Path(__file__)


class Initialize(CoreInitialize):

    def destroy_alembic_version(self):
        """删除迁移文件版本控制表"""
        self.destroy(table_name='alembic_version')

    def run(self):
        pass
