# -*- coding: utf-8 -*-

from application import create_app
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = create_app()
