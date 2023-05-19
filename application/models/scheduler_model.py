# -*- coding: utf-8 -*-
from . import db


class ApschedulerJobs(db.Model):
    ___tablename__ = 'apscheduler_jobs'

    id = db.Column(db.Unicode(191), primary_key=True, comment='任务ID')
    next_run_time = db.Column(db.Float(25), index=True, comment='任务下一次执行时间')
    job_state = db.Column(db.LargeBinary, nullable=False, comment='任务相关信息')
