#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine.py
@Time    :   2021/01/19 13:56:33
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class EhrEngine(object):
    """
    ehr相关操作
    """

    def __init__(self, name='ehr'):
        self._name = name

    def start(self):
        """
        docstring
        """
        return 'tt'


class PersonInfo(object):
    """
    ehr系统中人员信息
    """

    def __init__(self, complay="", depart="", branch="", assignment="", group="", code="", name="", professional="", gender="", nation="", birthday="", age=0, idNo="", personType="", sourceOfPerson="", timeOfWork="", timeOfJoinBaowu="", timeOfJoinComplay="", vJobTitle="", cJobTitle="", postType="", jobStatus=""):
        self._complayLevelOne = complay  # 一级机构(公司)
        self._departLevelTow = depart  # 二级机构（部门）
        self._branchLevelThree = branch  # 三级机构（分厂）
        self._assignmentSectionLevelFour = assignment  # 四级机构（作业区）
        self._groupLevelFive = group  # 五级机构（班组）
        self._code = code  # 职工编码
        self._name = name  # 姓名
        self._professional = professional  # 资格名称
        self._gender = gender  # 性别
        self._nation = nation  # 民族
        self._birthday = birthday  # 出生日期
        self._age = age  # 年龄
        self._certificateType = '居民身份证'  # 证件类型
        self._idNo = idNo  # 身份证号
        self._personType = personType  # 人员类型
        self._sourceOfPerson = sourceOfPerson  # 人员来源
        self._timeOfWork = timeOfWork  # 参加工作时间
        self._timeOfJoinBaowu = timeOfJoinBaowu  # 进入宝武时间
        self._timeOfJoinComplay = timeOfJoinComplay  # 进去公司时间
        self._vJobTile = vJobTitle  # 核定岗位名称
        self._cJobTitle = cJobTitle  # 执行岗位名称
        self._postType = postType  # 岗位类型
        self._jobStatus = jobStatus  # 人员类型

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_complayLevelOne"] = "一级机构(公司)"
        columns["_departLevelTow"] = "二级机构（部门)"
        columns["_branchLevelThree"] = "三级机构（分厂）"
        columns["_assignmentSectionLevelFour"] = "四级机构（作业区）"
        columns["_groupLevelFive"] = "五级机构（班组）"
        columns["_code"] = "职工编码"
        columns["_name"] = "姓名"
        columns["_professional"] = "资格名称"
        columns["_gender"] = "性别"
        columns["_nation"] = "民族"
        columns["_birthday"] = "出生日期"
        columns["_age"] = "年龄"
        columns["_certificateType"] = "证件类型"
        columns["_idNo"] = "身份证号"
        columns["_personType"] = "人员类型"
        columns["_sourceOfPerson"] = "人员来源"
        columns["_timeOfWork"] = "参加工作时间"
        columns["_timeOfJoinBaowu"] = "进入宝武时间"
        columns["_timeOfJoinComplay"] = "进去公司时间"
        columns["_vJobTile"] = "核定岗位名称"
        columns["_cJobTitle"] = "执行岗位名称"
        columns["_postType"] = "岗位类型"
        columns["_jobStatus"] = "人员类型"
        return columns

    def getPropertyName(self, columnName) -> str:
        """
        docstring
        """
        columns = self.getColumnDef()
        for key in columns.keys():
            if columns[key] == columnName:
                return key
        return ""
