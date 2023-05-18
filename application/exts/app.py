# -*- coding: utf-8 -*-
from flask import Flask as _Flask
from .json import DefaultJSONProvider


class Flask(_Flask):
    json_provider_class = DefaultJSONProvider

