#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine.py
@Time    :   2021/01/19 13:56:33
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import isfile
import xlrd


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
        personInfo = PersonInfo()
        cov = ExlToClazz(
            PersonInfo, personInfo.getColumnDef(), personInfo.get_exl_tpl_folder_path())
        persons = cov.loadTemp()

        salaryGzInfo = SalaryGzInfo()
        cov = ExlToClazz(
            SalaryGzInfo, salaryGzInfo.getColumnDef(), salaryGzInfo.get_exl_tpl_folder_path())
        salaryGzs = cov.loadTemp()

        salaryJjInfo = SalaryJjInfo()
        cov = ExlToClazz(
            SalaryJjInfo, salaryJjInfo.getColumnDef(), salaryJjInfo.get_exl_tpl_folder_path())
        salaryJjs = cov.loadTemp()

        return persons, salaryGzs, salaryJjs


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
        columns["_timeOfWork"] = "参加工作时间"
        columns["_timeOfJoinBaowu"] = "来宝钢系统日期"
        columns["_timeOfJoinComplay"] = "来公司日期"
        columns["_vJobTile"] = "核定岗位"
        columns["_cJobTitle"] = "执行岗位"
        columns["_postType"] = "岗位类型"
        columns["_jobStatus"] = "在职状态"
        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\人员信息.xls'

    def to_map(self, datas):
        m = dict()
        for i in len(datas):
            personInfo = datas[i]
            m[personInfo._code] = personInfo
        return m

    def __str__(self):
        return '员工基本信息: 公司 {} - 部门 {} - 分厂 {} - 作业区 {} - 班组 {} - 工号 {} - 姓名 {} - 岗位 {}'.format(self._complayLevelOne, self._departLevelTow, self._branchLevelThree, self._assignmentSectionLevelFour, self._groupLevelFive, self._code, self._name, self._cJobTitle)


class SalaryGzInfo(object):
    """
    工资信息
    """

    def __init__(self, code="", name="", departfullinfo="", depart="", branch="", salaryModel="", jobName="", postPrice="", distributionMark="", fzZxkc=0, fdZxkc=0, jxjyZxkc=0, totalPayable=0):
        self._code = code
        self._name = name
        self._departfullinfo = departfullinfo
        self._departLevelTow = depart
        self._branchLevelThree = branch
        self._salaryModel = salaryModel
        self._jobName = jobName
        self._postPrice = postPrice
        self._distributionMark = distributionMark
        self._fzZxkc = fzZxkc
        self._fdZxkc = fdZxkc
        self._jxjyZxkc = jxjyZxkc
        self._totalPayable = totalPayable

    def __str__(self):
        return '员工工资信息: 机构 {} - 二级机构 {} - 三级机构 {} - 工号 {} - 姓名 {} - 岗位 {} - 应发 {}'.format(self._departfullinfo, self._departLevelTow, self._branchLevelThree, self._code, self._name, self._jobName, self._totalPayable)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_departLevelTow"] = "二级机构"
        columns["_branchLevelThree"] = "三级机构"
        columns["_salaryModel"] = "薪酬模式"
        columns["_jobName"] = "岗位名称"
        columns["_postPrice"] = "岗位价值"
        columns["_distributionMark"] = "是否代发工资"
        columns["_fzZxkc"] = "累计住房租金支出"
        columns["_fdZxkc"] = "累计住房贷款利息支出"
        columns["_jxjyZxkc"] = "累计继续教育支出"
        columns["_totalPayable"] = "应发"
        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\工资信息-股份.xls'

    def to_map(self, datas):
        m = dict()
        for i in len(datas):
            info = datas[i]
            m[info._code] = info
        return m


class SalaryJjInfo(object):
    """
    奖金信息
    """

    def __init__(self, code="", name="", departfullinfo="", distributionMark="", ysjse=0, bonusTow=0, gtsyj=0, pay=0, jjhj=0, totalPayable=0, jsjseptsl=0, jbjj=0, gts=0, bonusOne=0, bonusThree=0, yseyhsl=0, yse=0, gstz=0):
        self._code = code
        self._name = name
        self._departfullinfo = departfullinfo
        self._distributionMark = distributionMark
        self._ysjse = ysjse
        self._bonusTwo = bonusTow
        self._gtsyj = gtsyj
        self._pay = pay
        self._jjhj = jjhj
        self._jsjseptsl = jsjseptsl
        self._jbjj = jbjj
        self._gts = gts
        self._bonusOne = bonusOne
        self._bonusThree = bonusThree
        self._yseyhsl = yseyhsl
        self._yse = yse
        self._totalPayable = totalPayable
        self._gstz = gstz

    def __str__(self):
        return '员工奖金信息: 机构 {} - 工号 {} - 姓名 {} - 应发 {} - 实发 {}'.format(self._departfullinfo, self._code, self._name, self._totalPayable, self._pay)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_distributionMark"] = "是否代发工资"
        columns["_ysjse"] = "应税计算额(优惠税率)"
        columns["_bonusTwo"] = "单项奖2"
        columns["_gtsyj"] = "个调税(应缴)"
        columns["_pay"] = "实发"
        columns["_jjhj"] = "奖金合计"
        columns["_jsjseptsl"] = "应税计算额(普通税率)"
        columns["_jbjj"] = "基本奖金"
        columns["_gts"] = "个调税"
        columns["_bonusOne"] = "单项奖1"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额(优惠税率)"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额"
        columns["_totalPayable"] = "应发"
        columns["gstz"] = "个税调整"

        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\奖金信息-股份.xls'

    def to_map(self, datas):
        m = dict()
        for i in len(datas):
            info = datas[i]
            m[info._code] = info
        return m


class ExlToClazz(object):
    """
    模板
    """

    def __init__(self, clazz, columnsDef, filePath):
        self.clazz = clazz
        self.columnsDef = columnsDef
        self.filePath = filePath

    def loadTemp(self) -> []:
        if not isfile(self.filePath):
            raise FileNotFoundError("文件路径 {0} 不存在".format(self.filePath))
        # 读取模板文件
        book = xlrd.open_workbook(self.filePath)
        # 读取第一个sheet 工作簿
        sheet = book.sheet_by_index(0)
        # 获取列头
        titles = sheet.row_slice(0)
        # 反射生成
        res = []
        for r in range(sheet.nrows):
            if r > 0:
                row = sheet.row_slice(r)
                ins = self.clazz()
                for i in range(len(titles)):
                    propertyName = self.getPropertyName(titles[i].value)
                    if "" != propertyName:
                        setattr(ins, propertyName, row[i].value)
                res.append(ins)

        return res

    def getPropertyName(self, columnName) -> str:
        """
        docstring
        """
        columns = self.columnsDef
        for key in columns.keys():
            if columns[key] == columnName:
                return key
        return ""
