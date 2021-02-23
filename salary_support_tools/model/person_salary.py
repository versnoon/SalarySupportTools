#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_salary.py
@Time    :   2021/02/19 12:57:28
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from salary_support_tools.engine.base_period_engine import BasePeriodEngine


class PersonSalaryInfo(BasePeriodEngine):
    """
    职工相关薪酬信息汇总
    """

    def __init__(self):
        super().__init__(None)
        self._depart = ""  # 审核单位信息
        self._depart_fullname = ""  # 机构全称
        self._tex_depart = ""  # 税务机构
        self._code = ""  # 职工编码
        self._name = ""  # 姓名
        self._idno = ""  # 身份证号
        self._gz = None  # 工资信息
        self._jj = None  # 奖金信息
        self._banks = None  # 银行信息
        self._person = None  # 员工基本信息
        self._job = None  # 岗位信息
        self._texes = None  # 税务信息
