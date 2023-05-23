### 环境

- 解释器版本：python 3.10.10
- 数据库: postgresql 14.6

### 一、部署 本地运行

##### 一、安装依赖

- 借助pycharm 创建虚拟环境

```shell
pip3 install --upgrade pip
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

##### 二、配置

- 复制 .env.example 文件并在同级目录创建 .env文件，进行相应环境变量的设置
- conf/setting.py 文件中配置常规环境依赖

##### 三、数据库迁移

- 先自行创建所需数据库 系统默认数据库名称：py.flask.scheduler

```shell
flask db init
flask db migrate -m '初始化'
flask db upgrade
```

##### 四、启动

```shell
flask run -h 0.0.0.0 -p {port}
```

### Docker 部署

##### 一、获取docker镜像

- 前提条件
    - win 环境本地已安装Docker Desktop
    - Linux 已安装Docker

```shell
# 进入项目根目录
cd py.flask.scheduler
# 执行
docker build -t apscheduler:lastet .
```

##### 二、启动docker镜像

```shell
# 将镜像运行获取容器
docker run -itd -p 41003:41003 -v 当前本地项目路径:/var/www/py.flask.scheduler --name apscheduler apscheduler

# 服务重启可更新项目依赖环境
docker restart 容器ID
```

##### 五、使用

- 动态添加JOB执行
- 通过config中的参数SCHEDULER_API_ENABLED已经开启flask_apscheduler的api，所以可以直接使用，下面是具体的api信息

```python
def _load_api(self):
    """
    Add the routes for the scheduler API.
    """
    self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
    self._add_url_route('add_job', '/jobs', api.add_job, 'POST')
    self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
    self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
    self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
    self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
    self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
    self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
    self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')
```

- 直接动态调用接口添加， 具体的参数需要到apscheduler的源码进行查看，就是通过apscheduler add_job的那些参数

```
请求添加接口：http://127.0.0.1:{port}/scheduler/jobs
请求方法：POST
请求header:
{
    "Content-Type": "application/json"
}
请求body:
{   
    "id": "id_get_current_datetime_date",
    "name": "获取当前时间",
    "func": "application:scheduler.jobs.get_current_datetime", #这里就是模块:包.py文件.方法名称
    "trigger": "date", # 触发器为指定时间，这里时间没有指定，就是立马执行
    "kwargs": {
        "name": "接口添加任务"
    },
    "replace_existing": True # 任务存在则进行修改
}
返回结果:
{
    "id": "id_get_current_datetime_date",
    "name": "获取当前时间",
    "func": "application:scheduler.jobs.get_current_datetime",
    "args": [],
    "kwargs": {
        "name": "用户名称"
    },
    "trigger": "date",
    "run_date": "2023-05-23T17:19:56.763788+08:00",
    "misfire_grace_time": 60,
    "max_instances": 3,
    "next_run_time": "2023-05-23T17:19:56.763788+08:00"
}
```