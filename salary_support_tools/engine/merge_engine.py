#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   merge_engine.py
@Time    :   2021/02/19 11:07:53
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from collections import OrderedDict

from salary_support_tools.model.person_salary import PersonSalaryInfo
from salary_support_tools.model.salary_gz import SalaryGz


class MergeEngine:
    """
    合并相关数据
    """

    def __init__(self, period, departs, persons, jobs, gzs, jjs, banks, texes=None):
        self._period = period  # 期间
        self._departs = departs  # 审核单位
        self._persons = persons  # 人员信息
        self._jobs = jobs  # 职位信息
        self._gzs = gzs  # 工资信息
        self._jjs = jjs  # 奖金信息
        self._banks = banks  # 银行卡信息
        self._texes = texes  # 税务系统相关信息

    def merge_salary_info(self):
        # 合并工资，奖金，银行卡信息，根据审核单位汇总
        # 合并工资奖金信息 获取完成得发放人员列表
        # 查询银行卡
        # 查询岗位
        # 查询税务信息
        res_tex_depart = dict()
        res_depart = dict()
        for tex_depart, gzs_by_depart in self._gzs.items():

            for depart, gzs in gzs_by_depart.items():
                for code, gz in gzs.items():
                    vs_tex_depart = dict()
                    vs_depart = dict()
                    if tex_depart in res_tex_depart:
                        vs_tex_depart = res_tex_depart[tex_depart]
                    if depart in res_depart:
                        vs_depart = res_depart[depart]
                    info = PersonSalaryInfo()
                    info.period = self._period
                    info._tex_depart = tex_depart
                    info._depart = depart
                    info._depart_fullname = gz._depart_fullname
                    info._gz = gz
                    info._code = code
                    info._job = self.get_person_salary_info(
                        self._jobs, tex_depart, depart, code)
                    info._jj = self.get_person_salary_info(
                        self._jjs, tex_depart, depart, code)
                    info._banks = self.get_person_salary_info(
                        self._banks, tex_depart, depart, code)
                    info._person = self.get_person_salary_info(
                        self._persons[0], tex_depart, depart, code)
                    info._texes = self.get_person_salary_info(
                        self._texes, tex_depart, depart, code)
                    vs_depart[code] = info
                    vs_tex_depart[depart] = vs_depart
                    res_depart[depart] = vs_depart
                    res_tex_depart[tex_depart] = vs_tex_depart
        for tex_depart, jjs_by_depart in self._jjs.items():
            for depart, jjs in jjs_by_depart.items():
                for code, jj in jjs.items():
                    jj_flag = True
                    if tex_depart in res_tex_depart:
                        if depart in res_tex_depart[tex_depart]:
                            if code in res_tex_depart[tex_depart][depart]:
                                jj_flag = False
                                continue
                    if jj_flag:
                        vs_tex_depart = dict()
                        vs_depart = dict()
                        if tex_depart in res_tex_depart:
                            vs_tex_depart = res_tex_depart[tex_depart]
                        if depart in res_depart:
                            vs_depart = res_depart[depart]
                        info = PersonSalaryInfo()
                        info.period = self._period
                        info._tex_depart = tex_depart
                        info._depart = depart
                        info._depart_fullname = jj._depart_fullname
                        info._jj = jj
                        info._code = code
                        info._job = self.get_person_salary_info(
                            self._jobs, tex_depart, depart, code)
                        info._banks = self.get_person_salary_info(
                            self._banks, tex_depart, depart, code)
                        info._person = self.get_person_salary_info(
                            self._persons[0], tex_depart, depart, code)
                        info._texes = self.get_person_salary_info(
                            self._texes, tex_depart, depart, code)
                        vs_depart[code] = info
                        vs_tex_depart[depart] = vs_depart
                        res_depart[depart] = vs_depart
                        res_tex_depart[tex_depart] = vs_tex_depart

        return res_tex_depart

    def get_person_salary_info(self, datas, tex_depart, depart, code):
        if tex_depart in datas:
            if depart in datas[tex_depart]:
                if code in datas[tex_depart][depart]:
                    return datas[tex_depart][depart][code]
        return None
