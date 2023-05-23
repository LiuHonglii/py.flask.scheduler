# -*- coding: utf-8 -*-
from datetime import datetime
from application.extensions.scheduler import custom_scheduler
from pprint import pprint


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

        pprint(jobs_list)

        # 此处无法写入日志原因：不存在请求上下文所导致
        # custom_scheduler.app.logger.info(f"test_job")


def get_current_datetime(*args, **kwargs):
    print(f'当前时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', (kwargs))


def get_summation(*args, **kwargs):
    """
    求和
    :param args:
    :param kwargs:
    :return:
    """
    print(f"求和结果:{sum(args)}")