# -*- coding: utf-8 -*-
from flask import current_app
from datetime import datetime
from application.exts import custom_scheduler
from application.models import ApschedulerJobs



def get_all_jobs():
    """
    测试job
    """
    with custom_scheduler.app.app_context():
        query_all = ApschedulerJobs.query.all()
        jobs_list = []
        for ele in query_all:
            jobs_list.append({
                'id':ele.id,
                'next_run_time':ele.next_run_time,
            })

        print(jobs_list)

        # 此处无法写入日志原因：不存在请求上下文所导致
        # custom_scheduler.app.logger.info(f"test_job")
