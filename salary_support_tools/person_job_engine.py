#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_job_engine.py
@Time    :   2021/02/05 15:32:49
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from salary_support_tools.exl_to_clazz import ExlsToClazz


class PersonJonEngine(object):
    """
    员工岗位聘用信息加载器
    """

    def __init__(self, period, departs):
        self._name = "person_job"
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'
        self._filename = "岗位聘用信息"

    def start(self):
        self.load_data()

    def load_data(self):
        job_info = PersonJob()  # 人员岗位聘用表
        person_job_load = ExlsToClazz(
            PersonJob, job_info.tpl_columns(), self.filepath_prefix(), self.filename_prefix())
        return self.to_map_by_company(
            person_job_load.loadTemp())

    def filepath_prefix(self):
        return r'{}\{}'.format(self._folder_path, self._period)

    def filename_prefix(self):
        return self._filename

    def to_map_by_company(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                jobInfo = datas[i]
                company, depart_str = self._get_depart_byfullname(
                    jobInfo._depart_fullname)
                jobs = []
                if company in m:
                    jobs = m[company]
                jobs.append(jobInfo)
                m[company] = jobs
        res = OrderedDict()
        for k, vs in m.items():
            res[k] = self.to_map_by_depart(vs)
        return res

    def _get_depart_byfullname(self, depart_fullname):
        departs = depart_fullname.split("\\")
        if len(departs) < 2:
            raise ValueError("{},机构信息异常".format(depart_fullname))
        depart_name = departs[1]
        for ds, depart in self._departs.items():
            if depart.is_depart(depart_name):
                depart_name = depart.get_depart_salaryScope_and_name()
                break

        return departs[0], depart_name

    def to_map_by_depart(self, datas):
        m = OrderedDict()
        for jobinfo in datas:
            company, depart_str = self._get_depart_byfullname(
                jobinfo._depart_fullname)
            jobs = OrderedDict()
            if depart_str in m:
                jobs = m[depart_str]
            jobs[jobinfo._code] = jobinfo
            m[depart_str] = jobs
        return m


class PersonJob(object):
    """
    员工岗位聘用信息
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

    def tpl_columns(self):
        columns = dict()
        columns["_code"] = "通行证"
        columns["_name"] = "姓名"
        columns["_depart_fullname"] = "机构名称"
        columns["_job_type"] = "岗位类型"
        columns["_hd_jobcode"] = "核定岗位编码"
        columns["_hd_jobname"] = "核定岗位名称"
        columns["_zx_jobcode"] = "执行岗位编码"
        columns["_zx_jobname"] = "执行岗位名称"
        columns["_job_m_level"] = "岗位管理层级"
        columns["_job_fullname"] = "组合(岗位序列+标准目录+岗位层级)"
        columns["_dy_type"] = "定员类型"
        columns["_bz"] = "班制"
        columns["_job_price"] = "岗位价值"
        columns["_job_time"] = "任职时间"
        columns["_job_overtime"] = "结束时间"
        columns["_fp_type"] = "分配类型"
        columns["_job_level"] = "岗位层级"
        columns["_job_level_type"] = "岗位层级(分类)"
        columns["_job_level_range"] = "岗级范围"
        return columns
