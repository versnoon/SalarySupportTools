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
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SalaryPerson(BasePeriodEngine):
    """
    员工相关信息
    """

    NAME = "salary_person"

    def __init__(self):
        super().__init__(None)
        self._complayLevelOne = ""  # 一级机构(公司)
        self._departLevelTow = ""  # 二级机构（部门）
        self._branchLevelThree = ""  # 三级机构（分厂）
        self._assignmentSectionLevelFour = ""  # 四级机构（作业区）
        self._groupLevelFive = ""  # 五级机构（班组）
        self._code = ""  # 职工编码
        self._name = ""  # 姓名
        self._professional = ""  # 资格名称
        self._gender = ""  # 性别
        self._nation = ""  # 民族
        self._birthday = ""  # 出生日期
        self._age = 0  # 年龄
        self._certificateType = '居民身份证'  # 证件类型
        self._idno = ""  # 身份证号
        self._personType = ""  # 人员类型
        self._sourceOfPerson = ""  # 人员来源
        self._timeOfWork = ""  # 参加工作时间
        self._timeOfJoinBaowu = ""  # 进入宝武时间
        self._timeOfJoinComplay = ""  # 进去公司时间
        self._vJobTile = ""  # 核定岗位名称
        self._cJobTitle = ""  # 执行岗位名称
        self._postType = ""  # 岗位类型
        self._jobStatus = ""  # 人员类型

    @classmethod
    def cols(self):
        cols = dict()
        cols["_complayLevelOne"] = "一级机构名称"
        cols["_departLevelTow"] = "二级机构名称"
        cols["_branchLevelThree"] = "三级机构名称"
        cols["_code"] = "通行证"
        cols["_name"] = "姓名"
        cols["_gender"] = "性别"
        cols["_idno"] = "证件号码"
        cols["_personType"] = "人员类型"
        cols["_timeOfWork"] = "参加工作日期"
        cols["_vJobTile"] = "岗位名称"
        cols["_jobStatus"] = "在职状态"
        return cols

    def __str__(self):
        return '员工基本信息: 工号 {} - 姓名 {} - 公司 {} - 部门 {} - 分厂 {} - 作业区 {} - 班组 {} - 岗位 {}'.format(self._code, self._name, self._complayLevelOne, self._departLevelTow, self._branchLevelThree, self._assignmentSectionLevelFour, self._groupLevelFive, self._cJobTitle)


class SalaryPersonConventor(BaseModelConventor):

    def cov(self, datas, period, departs):
        res_code = OrderedDict()
        res_idno = OrderedDict()
        for data in datas:
            vs_code = OrderedDict()
            vs_idno = OrderedDict()
            data.period = period
            companyname = data._complayLevelOne
            if not companyname:
                companyname = 'unknow'
            if companyname in res_code:
                vs_code = res_code[companyname]
            if companyname in res_idno:
                vs_idno = res_idno[companyname]
            if data._code:
                vs_code[data._code] = data
            if data._idno:
                vs_idno[data._idno] = data
            res_code[companyname] = vs_code
            res_idno[companyname] = vs_idno
        return res_code, res_idno
