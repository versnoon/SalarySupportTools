#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SalaryPeriod.py
@Time    :   2021/02/13 11:48:32
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from salary_support_tools.engine.base_period_engine import BasePeriodEngine


class SalaryJob(BasePeriodEngine):
    """
    员工岗位相关信息
    """

    def __init__(self):
        self._code = ""  # 通行证
        self._name = ""  # 姓名
        self._depart_fullname = ""  # 机构名称
        self._job_type = ""  # 岗位类型
        self._hd_jobcode = ""  # 核定岗位编码
        self._hd_jobname = ""  # 核定岗位名称
        self._zx_jobcode = ""  # 执行岗位编码
        self._zx_jobname = ""  # 执行岗位名称
        self._job_m_level = ""  # 岗位管理层级
        self._job_fullname = ""  # 组合(岗位序列+标准目录+岗位层级)
        self._dy_type = ""  # 定员类型
        self._bz = ""  # 班制
        self._job_price = ""  # 岗位价值
        self._job_time = ""  # 任职时间
        self._job_overtime = ""  # 结束时间
        self._fp_type = ""  # 分配类型
        self._job_level = ""  # 岗位层级
        self._job_level_type = ""  # 岗位层级(分类)
        self._job_level_range = ""  # 岗级范围

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "通行证"
        cols["_name"] = "姓名"
        cols["_depart_fullname"] = "机构名称"
        cols["_job_type"] = "岗位类型"
        cols["_hd_jobcode"] = "核定岗位编码"
        cols["_hd_jobname"] = "核定岗位名称"
        cols["_zx_jobcode"] = "执行岗位编码"
        cols["_zx_jobname"] = "执行岗位名称"
        cols["_job_m_level"] = "岗位管理层级"
        cols["_job_fullname"] = "组合(岗位序列+标准目录+岗位层级)"
        cols["_dy_type"] = "定员类型"
        cols["_bz"] = "班制"
        cols["_job_price"] = "岗位价值"
        cols["_job_time"] = "任职时间"
        cols["_job_overtime"] = "结束时间"
        cols["_fp_type"] = "分配类型"
        cols["_job_level"] = "岗位层级"
        cols["_job_level_type"] = "岗位层级(分类)"
        cols["_job_level_range"] = "岗级范围"
        return cols

    @classmethod
    def cov(self, datas, period):
        res = OrderedDict()
        for data in datas:
            vs_code = OrderedDict()
            data.period = period
        return res
