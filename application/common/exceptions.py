# -*- coding: utf-8 -*-
import traceback
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from . import error_resp


class CustomError(Exception):
    def __init__(self, msg=None, code='400', **kwargs):
        self.msg = msg
        self.code = code

    @staticmethod
    def _error_handler(error: Exception):
        """
        全局异常
        """
        code = '400'
        detail = traceback.format_exc()

        if isinstance(error, SQLAlchemyError):
            current_app.logger.error('[MySQL] {}'.format(detail))
            msg = 'MySQL Unavailable service.'
            if isinstance(error, IntegrityError):
                msg = "违反数据库唯一约束"

        elif isinstance(error, CustomError):
            current_app.logger.error('[CustomError] {}'.format(detail))
            msg, code = error.msg, error.code

        elif isinstance(error, TypeError):
            current_app.logger.error('[TypeError] {}'.format(detail))
            msg = error.args[0] if error.args else 'TypeError'

        else:
            current_app.logger.error('[Server Unknown Error] {}'.format(detail))
            msg = 'Server unknown error.'

        return error_resp(msg=msg, code=code)
