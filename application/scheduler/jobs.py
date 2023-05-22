# -*- coding: utf-8 -*-
from flask import current_app
from datetime import datetime
from application.extensions import custom_scheduler
from application.models import ApschedulerJobs


def get_all_jobs():
    """
    测试job
    """
    with custom_scheduler.app.app_context():
        query_all = custom_scheduler.get_jobs()
        jobs_list = []
        for ele in query_all:
            jobs_list.append({
                'id': ele.id,
                'next_run_time': ele.next_run_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        print(jobs_list)

        # 此处无法写入日志原因：不存在请求上下文所导致
        # custom_scheduler.app.logger.info(f"test_job")


def get_current_datetime(*args, **kwargs):
    print(f'当前时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', (args))
