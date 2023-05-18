# -*- coding: utf-8 -*-
__all__ = ['success_resp', 'error_resp']

from flask import jsonify


def success_resp(data=None, msg='OK', code='0', *args, **kwargs):
    # the return value should match the base response schema BaseResponseSchema
    # and the data key should match
    data = {
        'code': str(code),
        'msg': msg,
        'data': data,
    }

    return jsonify(data, *args, **kwargs)


def error_resp(data=None, msg='ERROR', code='400', *args, **kwargs):
    # the return value should match the base response schema BaseResponseSchema
    # and the data key should match
    data = {
        'code': str(code),
        'msg': msg,
        'data': data,
    }
    return jsonify(data, *args, **kwargs)
