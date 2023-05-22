#!/bin/bash
# 功能:docker ENTRYPOINT
# 脚本名：docker-entrypoint.sh
# 作者：Hongli Liu
# 版本：V 1.0

pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
# 删除版本控制表以及版本控制文件
flask del-alembic-version
# 删除版本迁移文件
flask del-migrations
# 生成版本迁移文件
flask db init
flask db migrate
flask db upgrade
# 初始化字典
#flask init-dict
# 初始化数据
#flask init-db

gunicorn -c gconfig.py -b 0.0.0.0:41003
