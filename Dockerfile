FROM python:3.10.10

RUN mkdir -p /py.flask.scheduler

COPY ./ /py.flask.scheduler

WORKDIR /py.flask.scheduler

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

#ENTRYPOINT ["gunicorn", "-c", "g.conf.py", "-b", "0.0.0.0:9800"]
ENTRYPOINT ["./docker-entrypoint.sh"]