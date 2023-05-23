FROM python:3.10.10
# 设置编码
ENV LANG en_US.UTF-8
# 设置时区
ENV TZ Asia/Shanghai

RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone

RUN mkdir -p /py.flask.scheduler

COPY . /var/www/py.flask.scheduler/

WORKDIR /var/www/py.flask.scheduler/

# 更新
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
# 声明容器段端口
#EXPOSE 41003

# 执行脚本文件
#COPY docker-entrypoint.sh /usr/local/bin/
#RUN chmod +x /usr/local/bin/docker-entrypoint.sh

#ENTRYPOINT ["gunicorn", "-c", "gconfig.py", "-b", "0.0.0.0:9800"]
ENTRYPOINT ["./docker-entrypoint.sh"]