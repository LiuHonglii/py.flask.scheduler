# -*- coding: utf-8 -*-
import logging
import threading
from application.extensions.scheduler import custom_scheduler
from application.models import ApschedulerJobInfo, db
from application.models import ApschedulerJobEvent
from apscheduler.events import (EVENT_JOB_ERROR,
                                EVENT_JOB_MISSED,
                                EVENT_JOB_MAX_INSTANCES,
                                EVENT_ALL_JOBS_REMOVED,
                                EVENT_JOB_ADDED,
                                EVENT_JOB_REMOVED,
                                EVENT_JOB_MODIFIED,
                                EVENT_JOB_EXECUTED,
                                EVENT_JOB_SUBMITTED)
from application.common import CustomError

LOGGER = logging.getLogger('flask_apscheduler')

STATUS_MAPPING = {
    EVENT_JOB_ADDED: 0,
    EVENT_JOB_MODIFIED: 1,
    EVENT_JOB_SUBMITTED: 2,
    EVENT_JOB_EXECUTED: 3,
    EVENT_JOB_REMOVED: 4,
    EVENT_JOB_ERROR: 5,
    EVENT_JOB_MISSED: 6,
    EVENT_ALL_JOBS_REMOVED: 7,
    EVENT_JOB_MAX_INSTANCES: 8
}


def listener_all_job(event):
    """
    监控job的生命周期，可视化监控，并且可增加后续的没有触发任务等监控
    添加到线程做处理
    :param event:触发事件
    :return:
    """
    job_id = None
    kw = {}
    if event.code != EVENT_ALL_JOBS_REMOVED:
        job_id = event.job_id
    if job_id:
        job = custom_scheduler.get_job(id=job_id, jobstore=event.jobstore)
        if job:
            kw = {
                'job_name': job.name,
                'job_func': str(job.func_ref),
                'job_trigger': job.trigger if isinstance(job.trigger, str) else str(job.trigger).split("[")[0],
                'job_next_run_time': str(job.next_run_time).split(".")[0],
            }
    kw |= {
        'job_id': job_id,
        'event_type': event.code,
        'job_traceback': event.traceback if hasattr(event, 'traceback') else "",
    }
    handle_listener_all_job(**kw)

    # t = threading.Thread(target=handle_listener_all_job, kwargs=kw)
    # t.start()
    # t.join()


def handle_listener_all_job(event_type, job_id, job_traceback='', **kwargs):
    """
    实际处理IO操作
    如何处理一个job_id重复使用的问题，采用本地id自增，如果真有job_id重复的情况，则认f为{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的是最后一个job_id对应的任务
    """
    with custom_scheduler.app.app_context():
        with db.auto_commit():
            try:
                if event_type == EVENT_JOB_ADDED:
                    # 添加任务定义表
                    job = ApschedulerJobInfo(job_status=0, job_id=job_id, **kwargs)
                    db.session.add(job)
                    db.session.flush()
                    # 增加任务事件表
                    job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                    db.session.add(job_event)
                elif event_type == EVENT_JOB_MODIFIED:
                    # 修改job[取数据库表中job_id最后一个进行修改]
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        for k, v in kwargs.items():
                            setattr(job, k, v)
                        job.job_status = 0
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
                elif event_type == EVENT_JOB_SUBMITTED:
                    # 提交job执行
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
                elif event_type == EVENT_JOB_EXECUTED:
                    # 执行job
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        job.job_status = 1

                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在 {job_id}")
                elif event_type == EVENT_JOB_REMOVED:
                    # 删除job
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        job.job_status = 5

                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
                elif event_type == EVENT_JOB_ERROR:
                    # 执行job出错
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        job.job_status = 2
                        job.job_traceback = job_traceback
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
                elif event_type == EVENT_JOB_MISSED:
                    # job执行错过
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        job.job_status = 3
                        job.job_traceback = job_traceback
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
                elif event_type == EVENT_ALL_JOBS_REMOVED:
                    # 删除所有job
                    all_jobs = ApschedulerJobInfo.query.filter(ApschedulerJobInfo.job_status == 0).all()
                    for job in all_jobs:
                        job.job_status = 6
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                elif event_type == EVENT_JOB_MAX_INSTANCES:
                    # job超过最大实例
                    job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                        ApschedulerJobInfo.job_id == job_id).first()
                    if job:
                        # 更新JOB表
                        job.job_status = 4
                        job.job_traceback = job_traceback
                        # 增加任务事件表
                        job_event = ApschedulerJobEvent(job_info_id=job.id, event=STATUS_MAPPING[event_type])
                        db.session.add(job_event)
                    else:
                        LOGGER.warning(f"{ApschedulerJobEvent.EVENT_MAPPING[STATUS_MAPPING[event_type]]} 指定的job本地不存在{job_id}")
            except:
                raise CustomError('执行任务异常')


# 添加事件监听
custom_scheduler.add_listener(listener_all_job,
                              EVENT_JOB_ERROR
                              | EVENT_JOB_MISSED
                              | EVENT_JOB_MAX_INSTANCES
                              | EVENT_ALL_JOBS_REMOVED
                              | EVENT_JOB_ADDED
                              | EVENT_JOB_REMOVED
                              | EVENT_JOB_MODIFIED
                              | EVENT_JOB_EXECUTED
                              | EVENT_JOB_SUBMITTED
                              )
