#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_salary_engine.py
@Time    :   2021/01/29 10:33:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from collections import OrderedDict


class PersonSalaryEngine(object):

    def __init__(self, period, persons, gzs, jjs, banks):
        self._name = "person_salary"
        self._period = period  # 期间
        self._gzs = gzs   # 工资
        self._jjs = jjs  # 奖金
        self._persons = persons  # 人员信息集合
        self._banks = banks  # 银行信息

    def start(self):
        """
        组装人员的薪酬信息 包括 persons code depart
        """
        datas = self.merge_salary_info(self._gzs, self._jjs)
        self.merge_salary_person_bank_info(self._persons, self._banks, datas)

    def merge_salary_info(self, gzs, jjs):
        # 根据单位分组工资奖金数据
        infos = OrderedDict()
        for code, gz in gzs.items():
            info = PersonSalaryInfo()
            info._period = self._period  # 期间信息
            info._depart = gz.depart  # 单位信息
            info._gz = gz  # 工资信息
            vs = OrderedDict()
            if info._depart in infos:
                vs = infos[info._depart]
            vs[code] = info
            infos[info._depart] = vs
        for code, jj in jjs.items():
            jj_depart_str = jj.depart
            vs = OrderedDict()
            if jj_depart_str in infos:
                vs = infos[jj_depart_str]
            info = PersonSalaryInfo()
            if code in vs:
                info = vs[code]
            else:
                info._period = self._period  # 期间信息
                info._depart = jj.depart  # 单位信息
            info._jj = jj  # 奖金信息
            vs[code] = info
            infos[info._depart] = vs
        return infos

    def merge_salary_person_bank_info(self, persons, banks, person_salary_infos):
        # 合并人员数据
        for depart_str, psis in person_salary_infos.items():
            for code, psi in psis.items():
                person, person_flag = self.get_person(code, persons)
                if person is not None:
                    psi._person = person
                    psi._person_flag = person_flag
                if depart_str in banks:
                    banks_info = banks[depart_str]
                    if code in banks_info:
                        banks = banks_info[code]
                        psi._banks = banks

    def get_person(self, code, persons):
        person = None
        if code in persons["c"]:  # 当前人员信息
            person = persons["c"][code]
            return person, "c"
        elif code in persons["o"]:  # 上期人员信息
            person = persons["o"][code]
            return person, "o"
        else:
            person = persons["o_o"][code]
            return person, "o_o"
        return person, ""


class PersonSalaryInfo(object):
    """
    个人薪酬信息
    """

    def __init__(self, period="", depart="", person=None, code="", gz=None, jj=None, banks=None):
        self._period = period
        self._depart = depart
        self._code = code
        self._gz = gz
        self._jj = jj
        self._banks = banks
        self._person = person
        self._person_flag = "c"  # "current"
