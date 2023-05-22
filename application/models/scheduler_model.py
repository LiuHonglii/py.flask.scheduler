# -*- coding: utf-8 -*-
from datetime import datetime
from . import db


class ApschedulerJobs(db.Model):
    """JOB 信息"""
    ___tablename__ = 'apscheduler_jobs'

    id = db.Column(db.Unicode(191), primary_key=True, comment='任务ID')
    next_run_time = db.Column(db.Float(25), index=True, comment='任务下一次执行时间')
    job_state = db.Column(db.LargeBinary, nullable=False, comment='任务相关信息')


class ApschedulerJobInfo(db.Model):
    """JOB 详情表"""
    __tablename__ = "apscheduler_job_info"

    JOB_STATUS_MAPPING = {
        0: "待执行",
        1: "执行完成",
        2: "执行异常",
        3: "未执行结束",
        4: "系统异常",
        5: "已删除",
        6: "批量删除"
    }

    id = db.Column(db.Integer, primary_key=True, comment="id 主键，用于防止JObID多次使用的情况")
    job_id = db.Column(db.String(200), nullable=False, comment="JOBID")
    job_name = db.Column(db.String(200), comment="JOB名字")
    job_trigger = db.Column(db.String(30), comment="触发类型")
    job_func = db.Column(db.String(200), comment="执行的函数信息")
    job_next_run_time = db.Column(db.String(30), comment="JOB下次执行时间")
    job_status = db.Column(db.Integer, nullable=False, comment="JOB 状态 0:待执行 1:执行完成 2:执行异常 3:未执行结束 4:系统异常 5:已删除 6:批量删除")
    job_traceback = db.Column(db.TEXT, comment="执行报错时的错误信息")
    create_time = db.Column(db.TIMESTAMP(True), nullable=False, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.TIMESTAMP(True), nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    events = db.relationship('ApschedulerJobEvent', backref='job_info', cascade='all, delete')

    def __repr__(self):
        return self.job_id


class ApschedulerJobEvent(db.Model):
    """JOB 事件表"""
    __tablename__ = "apscheduler_job_event"

    EVENT_MAPPING = {
        0: "添加JOB",
        1: "修改JOB",
        2: "提交JOB",
        3: "执行JOB",
        4: "删除JOB",
        5: "执行JOB异常",
        6: "执行JOB过期",
        7: "全量删除JOB",
        8: "JOB超过最大实例数"
    }

    id = db.Column(db.Integer, primary_key=True, comment="id 主键，用于防止JObID多次使用的情况")
    job_info_id = db.Column(db.Integer, db.ForeignKey('apscheduler_job_info.id'), comment="JOB_INFO_ID")
    event = db.Column(db.Integer,
                      comment="JOB事件 0:添加JOB 1:修改JOB 2:提交JOB 3:执行JOB 4:删除JOB 5:执行JOB异常 6:执行JOB过期 7:全量删除JOB 8:JOB超过最大实例数")
    create_time = db.Column(db.TIMESTAMP(True), nullable=False, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return "<<event:{}>>".format(self.EVENT_MAPPING.get(self.event, self.event))
