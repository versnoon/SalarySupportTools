#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_engine.py
@Time    :   2021/01/28 12:04:31
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import exists
from os import makedirs

from collections import OrderedDict

from salary_support_tools.exl_to_clazz import ExlToClazz, ExlsToClazz


class PersonEngine(object):
    """
    人员信息处理引擎
    """

    def __init__(self, period):
        self._name = "person"
        self._period = period
        self._folder_path = r'd:\薪酬审核文件夹'
        self._person_info_filename = "人员信息导出结果"
        self._filename = '人员信息.xls'
        self._older_filename = '上期人员信息.xls'
        self._old_old_filename = '上上期人员信息.xls'
        self._persons = []  # 本期人员信息
        self.old_persons = []  # 上期人员信息

    def start(self):
        ps = self.loadPersonData()
        messages = self.comparePerson(ps)
        self.write_to(messages)

    def loadPersonData(self):
        """
        加载人员信息
        """
        res = dict()
        # person_info = PersonInfo()
        # person_load = ExlToClazz(
        #     PersonInfo, person_info.getColumnDef(), self.get_tpl_path())
        # persons = person_info.to_map_by_company(person_load.loadTemp())
        # res["c"] = persons
        person_info = PersonInfo()  # 人员信息维护表
        person_load_new = ExlsToClazz(
            PersonInfo, person_info.get_person_maintain_info_columns(), self.filepath_prefix(), self.filename_prefix())
        current_persons = person_info.to_map_by_company(
            person_load_new.loadTemp())
        res["c"] = current_persons
        old_person_load = ExlToClazz(
            PersonInfo, person_info.getColumnDef(), self.get_old_tpl_path())
        old_persons = person_info.to_map_by_company(old_person_load.loadTemp())
        res["o"] = old_persons
        old_old_person_load = ExlToClazz(
            PersonInfo, person_info.getColumnDef(), self.get_old_old_tpl_path())
        old_old_persons = person_info.to_map_by_company(
            old_old_person_load.loadTemp())
        res["o_o"] = old_old_persons

        return res

    def load_data_new(self):
        res = dict()
        person_new = PersonInfo()  # 人员信息维护表
        person_load_new = ExlsToClazz(
            PersonInfo, person_new.get_person_maintain_info_columns(), self.filepath_prefix(), self.filename_prefix())
        current_persons = person_new.to_map_by_company(
            person_load_new.loadTemp())
        res["c"] = current_persons
        return res

    def load_data(self):
        res = dict()
        person_info = PersonInfo()
        person_load_new = ExlsToClazz(
            PersonInfo, person_info.get_person_maintain_info_columns(), self.filepath_prefix(), self.filename_prefix())
        current_persons = person_info.to_map_by_company(
            person_load_new.loadTemp())
        res["c"] = current_persons
        old_person_load = ExlToClazz(
            PersonInfo, person_info.getColumnDef(), self.get_old_tpl_path(), titleindex=0, noneable=True)
        old_persons = person_info.to_map(old_person_load.loadTemp())
        res["o"] = old_persons
        old_old_person_load = ExlToClazz(
            PersonInfo, person_info.getColumnDef(), self.get_old_old_tpl_path(), titleindex=0, noneable=True)
        old_old_persons = person_info.to_map(
            old_old_person_load.loadTemp())
        res["o_o"] = old_old_persons
        return res

    def filepath_prefix(self):
        return r'{}\{}'.format(self._folder_path, self._period)

    def filename_prefix(self):
        return self._person_info_filename

    def get_tpl_path(self):
        return r'{}\{}\{}'.format(self._folder_path, self._period, self._filename)

    def get_old_tpl_path(self):
        return r'{}\{}\{}'.format(self._folder_path, self._period, self._older_filename)

    def get_old_old_tpl_path(self):
        return r'{}\{}\{}'.format(self._folder_path, self._period, self._old_old_filename)

    def comparePerson(self, persons):
        """
        对比两期数据,分类
        """
        msgs = dict()
        vs = self.get_perons_by_flag(persons)
        for k, ps in vs.items():
            ops = self.get_perons_by_flag(persons, "o")[k]
            oops = self.get_perons_by_flag(persons, "o")[k]
            msgs[k] = self.compare_detail(ps, ops, oops)
        return msgs

    def get_perons_by_flag(self, persons, flag="c"):
        return persons[flag]

    def compare_detail(self, persons, old_persons, old_old_persons):
        res = []
        for k, p in persons.items():
            # 增员人员
            if k not in old_persons:
                res.append(self.get_msg(p, "增员"))
        for k, op in old_persons.items():
            # 奖金发放人员
            if k not in persons:
                res.append(self.get_msg(op, "r减员[奖金发放]"))
        for k, op in old_old_persons.items():
            # 减员人员
            if k not in persons:
                res.append(self.get_msg(op, "减员[税务减员]"))
        return res

    def get_msg(self, person, msg):
        return r'人员变化类型 {},人员信息 {}'.format(msg, person)

    def write_to(self, msgs):
        for k, messages in msgs.items():
            if len(messages) > 0:
                path_prefix = r'{}\{}\{}\{}'.format(
                    self._folder_path, self._period, "人员变化情况", k)
                if not exists(path_prefix):
                    makedirs(path_prefix)
                path = r'{}\{}_{}_{}'.format(
                    path_prefix, k, self._period, "人员变化情况.txt")

                with open(path, 'a', encoding='utf-8') as f:
                    for m in messages:
                        f.write(m + '\n')

    def merge_persions(self):
        """
        合并
        """


class PersonInfo(object):
    """
    ehr系统中人员信息
    """

    def __init__(self, complay="", depart="", branch="", assignment="", group="", code="", name="", professional="", gender="", nation="", birthday="", age=0, idNo="", personType="", sourceOfPerson="", timeOfWork="", timeOfJoinBaowu="", timeOfJoinComplay="", vJobTitle="", cJobTitle="", postType="", jobStatus=""):
        self.period = ""
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

    def get_person_maintain_info_columns(self) -> dict:
        columns = dict()
        columns["_complayLevelOne"] = "一级机构名称"
        columns["_departLevelTow"] = "二级机构名称"
        columns["_branchLevelThree"] = "三级机构名称"
        columns["_code"] = "通行证"
        columns["_name"] = "姓名"
        columns["_gender"] = "性别"
        columns["_idNo"] = "证件号码"
        columns["_personType"] = "人员类型"
        columns["_timeOfWork"] = "参加工作日期"
        columns["_vJobTile"] = "岗位名称"
        columns["_jobStatus"] = "在职状态"
        return columns

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_complayLevelOne"] = "一级机构(公司)"
        columns["_departLevelTow"] = "二级机构(部门)"
        columns["_branchLevelThree"] = "三级机构(分厂)"
        columns["_assignmentSectionLevelFour"] = "四级机构(作业区)"
        columns["_groupLevelFive"] = "五级机构(班组)"
        columns["_code"] = "工号"
        columns["_name"] = "姓名全称"
        columns["_professional"] = "资格名称"
        columns["_gender"] = "性别"
        columns["_nation"] = "民族"
        columns["_birthday"] = "出生日期"
        columns["_age"] = "年龄"
        columns["_certificateType"] = "证件类型"
        columns["_idNo"] = "证件号码"
        columns["_personType"] = "人员类型"
        columns["_sourceOfPerson"] = "人员来源"
        columns["_timeOfWork"] = "参加工作日期"
        columns["_timeOfJoinBaowu"] = "来宝钢系统日期"
        columns["_timeOfJoinComplay"] = "来公司日期"
        columns["_vJobTile"] = "核定岗位"
        columns["_cJobTitle"] = "执行岗位"
        columns["_postType"] = "岗位类型"
        columns["_jobStatus"] = "在职状态"
        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\{}\人员信息.xls'.format(self.period)

    def to_map(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                personInfo = datas[i]
                m[personInfo._code] = personInfo
        return m

    def to_map_by_idno(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                personInfo = datas[i]
                m[personInfo._idNo] = personInfo
        return m

    def to_map_by_company(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                personInfo = datas[i]
                key = personInfo._complayLevelOne
                persons = []
                if key in m:
                    persons = m[key]
                persons.append(personInfo)
                m[personInfo._complayLevelOne] = persons
        res = OrderedDict()
        for k, vs in m.items():
            res[k] = self.to_map(vs)
        return res

    def __str__(self):
        return '员工基本信息: 工号 {} - 姓名 {} - 公司 {} - 部门 {} - 分厂 {} - 作业区 {} - 班组 {} - 岗位 {}'.format(self._code, self._name, self._complayLevelOne, self._departLevelTow, self._branchLevelThree, self._assignmentSectionLevelFour, self._groupLevelFive,  self._cJobTitle)
