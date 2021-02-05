#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_engine.py
@Time    :   2021/02/04 11:21:04
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class PersonCompareEngine(object):

    def __init__(self, period=None, departs=None, current_persons=None, person_salary_infos=None):
        self._name = 'person_compare'
        self._period = period
        self._departs = departs
        self._current_persons = current_persons  # ehr 导出得当期人员数据
        self._person_salary_infos = person_salary_infos  # 上期薪酬发放数据
        self._folder_path = r'd:\薪酬审核文件夹'

    def start(self):

        incs = dict()
        reds = dict()
        for depart_str, c_ps in self._current_persons.items():
            vs = dict()
            c_ps = self._current_persons[depart_str]
            if depart_str in self._person_salary_infos:
                pre_ps = self._person_salary_infos[depart_str]
                inc, red = self.compare_detail(depart_str, c_ps, pre_ps)
                incs[depart_str] = inc
                reds[depart_str] = red
        return incs, reds

    def compare_detail(self, depart_str, current_persons, pre_persons):
        # 新增
        # 减少 （发奖金，净减员）
        increase = self.increase_person_info(
            depart_str, current_persons, pre_persons)
        reduce = self.reduce_person_info(
            depart_str, current_persons, pre_persons)
        return increase, reduce

    def increase_person_info(self, depart_str, current_persons, pre_persons):
        """
        新增人员
        """
        res = []
        for code, person in current_persons.items():
            if code not in pre_persons:
                res.append(PersonChangeInfo(
                    self._period, depart_str, code, person, "新增人员"))
        return res

    def reduce_person_info(self, depart_str, current_persons, pre_persons):
        """
        减员人员
        """
        res = []
        for code, person_salary_info in pre_persons.items():
            if code not in current_persons:
                if person_salary_info._gz is not None and person_salary_info._gz._totalPayable != 0 and person_salary_info._jj is not None and person_salary_info._jj._totalPayable != 0:  # 有工资奖金得减员
                    res.append(PersonChangeInfo(
                        self._period, depart_str, code, person_salary_info._person, "减员人员-奖金"))
                elif person_salary_info._gz is None and person_salary_info._jj is not None and person_salary_info._jj._totalPayable != 0:

                    res.append(PersonChangeInfo(self._period, depart_str, code,
                                                person_salary_info._person, "减员人员-净减员"))
        return res

    def pre_period(self):
        month = 0
        year = 0
        try:
            month = int(self._period[:2])
            year = int(self._period[4:])
        except ValueError:
            return "000000"
        if month >= 12:
            month = 1
            year -= 1
        else:
            month -= 1
        return "{:0>4d}{:0>2d}".format(year, month)

    def columns_def(self):
        columns = dict()
        columns["_period"] = "期间"
        columns["_depart_str"] = "机构"
        columns["_code"] = "人员信息"
        columns["_changeinfo"] = "变更类型"
        return columns


class PersonChangeInfo(object):

    def __init__(self, period, depart_str, code, person, changeinfo):
        self._period = period
        self._depart_str = depart_str
        self._person = person
        self._code = code
        self._changeinfo = changeinfo

    def __str__(self):
        return '人员变化信息: 变化类别 {} - 职工编码 {} -期间 {} - 公司 {}'.format(self._changeinfo, self._code, self._period, self._depart_str)
