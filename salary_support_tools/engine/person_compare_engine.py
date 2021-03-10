#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_engine.py
@Time    :   2021/02/25 11:53:17
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools.engine.load_tpls_engine import LoadTplEngine


class PersonCompareEngine:

    def compare(self):
        """
        对比信息
        """
        load_engine = LoadTplEngine()

        current_period, departs = load_engine.load_current_period_departs()

        persons = load_engine.load_persons(current_period, departs)

        pre_period = load_engine.pre_period(current_period)

        pre_period, pre_departs, pre_persons, pre_jobs, pre_gzs, pre_jjs, pre_banks, pre_texes, pre_merge_infos = load_engine.load_tpl_by_period(
            pre_period)

        incs_by_tex_depart, reds_by_tex_depart = self.create_compare_infos_by_tex_depart(
            current_period, persons[0], pre_merge_infos, pre_persons[0])
        incs_by_depart, reds_by_depart = self.create_compare_infos_by_depart(
            current_period, persons[0], pre_merge_infos, pre_persons[0])

        return incs_by_tex_depart, reds_by_tex_depart, incs_by_depart, reds_by_depart

    def create_compare_infos_by_depart(self, period, current_persons, pre_person_salary_infos, pre_all_persons):

        res_incs = dict()
        res_reds = dict()
        for tex_depart, c_ps_by_tex_depart in current_persons.items():

            if tex_depart == "unknow":
                continue
            vs_incs_depart = dict()
            vs_incs = dict()
            vs_reds_depart = dict()
            vs_reds = dict()
            if tex_depart in res_incs:
                vs_incs_depart = res_incs[tex_depart]
            if tex_depart in res_reds:
                vs_reds_depart = res_reds[tex_depart]
            for depart, c_ps_by_depart in c_ps_by_tex_depart.items():
                if depart in vs_incs_depart:
                    vs_incs = vs_incs_depart[depart]
                if depart in vs_reds_depart:
                    vs_reds = vs_reds_depart[depart]
                pre_ps = dict()
                if tex_depart in pre_person_salary_infos:
                    if depart in pre_person_salary_infos[tex_depart]:
                        pre_ps = pre_person_salary_infos[tex_depart][depart]
                inc, red = self.compare_detail_by_depart(
                    period, depart, c_ps_by_depart, pre_ps, pre_all_persons)
                vs_incs[depart] = inc
                vs_reds[depart] = red
                vs_incs_depart[tex_depart] = vs_incs
                vs_reds_depart[tex_depart] = vs_reds
                res_incs[tex_depart] = vs_incs
                res_reds[tex_depart] = vs_reds
        return res_incs, res_reds

    def create_compare_infos_by_tex_depart(self, period, current_persons, pre_person_salary_infos, pre_all_persons):

        incs = dict()
        reds = dict()
        for tex_depart, c_ps in current_persons.items():
            if tex_depart == "unknow":
                continue
            vs = dict()
            if tex_depart in pre_person_salary_infos:
                pre_ps = pre_person_salary_infos[tex_depart]
                inc, red = self.compare_detail(
                    period, tex_depart, c_ps, pre_ps, pre_all_persons)
                incs[tex_depart] = inc
                reds[tex_depart] = red
        return incs, reds

    def compare_detail_by_depart(self, period, tex_depart, current_persons, pre_persons, pre_all_persons):
        # 新增
        # 减少 （发奖金，净减员）
        increase = self.increase_person_info_by_depart(period,
                                                       tex_depart, current_persons, pre_persons)
        reduce = self.reduce_person_info_by_depart(period,
                                                   tex_depart, current_persons, pre_persons, pre_all_persons)
        return increase, reduce

    def compare_detail(self, period, tex_depart, current_persons, pre_persons, pre_all_persons):
        # 新增
        # 减少 （发奖金，净减员）
        increase = self.increase_person_info(period,
                                             tex_depart, current_persons, pre_persons)
        reduce = self.reduce_person_info(period,
                                         tex_depart, current_persons, pre_persons, pre_all_persons)
        return increase, reduce

    def increase_person_info_by_depart(self, preiod, depart, current_persons, pre_persons):
        """
        新增人员
        """
        res = []

        for code, person in current_persons.items():
            if not pre_persons:
                res.append(PersonChangeInfo(
                    preiod, depart, code, person._idno, person._name, person._departLevelTow, "新增人员", person._tel))
            if pre_persons and code not in pre_persons:
                res.append(PersonChangeInfo(
                    preiod, depart, code, person._idno, person._name, person._departLevelTow, "新增人员", person._tel))
        return res

    def increase_person_info(self, preiod, tex_depart, current_persons, pre_persons):
        """
        新增人员
        """
        res = []
        cps = self.get_tex_depart_persons(current_persons)
        rps = self.get_tex_depart_persons(pre_persons)

        for code, person in cps.items():
            if code not in rps:
                res.append(PersonChangeInfo(
                    preiod, tex_depart, code, person._idno, person._name, person._departLevelTow, "新增人员", person._tel))
        return res

    def reduce_person_info_by_depart(self, preiod, depart, current_persons, pre_persons, texes):
        """
        减员人员
        """
        res = []
        for code, person_salary_info in pre_persons.items():
            if code not in current_persons:
                idno, tel = self.get_idno(person_salary_info, texes)
                name = person_salary_info[0]._name
                full_departname = person_salary_info[0]._depart_fullname
                if person_salary_info[0]._gz is not None and person_salary_info[0]._gz._totalPayable != 0 and person_salary_info[0]._jj is not None and person_salary_info[0]._jj._totalPayable != 0:  # 有工资奖金得减员
                    res.append(PersonChangeInfo(
                        preiod, depart, code, idno, name, full_departname, "减员人员-奖金", tel))
                else:
                    if person_salary_info[0]._gz is not None and (person_salary_info[0]._jj is None or person_salary_info[0]._jj._totalPayable == 0):
                        res.append(PersonChangeInfo(preiod, depart, code,
                                                    idno, name, full_departname, "减员人员-净减员", tel))
        return res

    def reduce_person_info(self, preiod, tex_depart, current_persons, pre_persons, texes):
        """
        减员人员
        """
        res = []
        res = []
        cps = self.get_tex_depart_persons(current_persons)
        rps = self.get_tex_depart_persons(pre_persons)
        for code, person_salary_info in rps.items():
            if code not in cps:
                idno, tel = self.get_idno(person_salary_info, texes)
                name = person_salary_info[0]._name
                full_departname = person_salary_info[0]._depart_fullname
                if person_salary_info[0]._gz is not None and person_salary_info[0]._gz._totalPayable != 0 and person_salary_info[0]._jj is not None and person_salary_info[0]._jj._totalPayable != 0:  # 有工资奖金得减员

                    res.append(PersonChangeInfo(
                        preiod, tex_depart, code, idno, name, full_departname, "减员人员-奖金", tel))
                else:
                    if person_salary_info[0]._gz is not None and (person_salary_info[0]._jj is None or person_salary_info[0]._jj._totalPayable == 0):
                        res.append(PersonChangeInfo(preiod, tex_depart, code,
                                                    idno, name, full_departname, "减员人员-净减员", tel))
        return res

    def get_tex_depart_persons(self, persons_by_depart):
        res = dict()
        for depart, persons in persons_by_depart.items():
            res = dict(res, **persons)
        return res

    def get_idno(self, person_salary_info, pre_all_persons=None):
        idno, tel = "", ""
        if person_salary_info[0]:
            person = person_salary_info[0]._person
            if person:
                idno = person._idno
                tel = person._tel
        if not idno or not tel:
            if person_salary_info[1]:  # sapinfo
                if person_salary_info[1]._idno:
                    idno = person_salary_info[1]._idno
            if pre_all_persons:
                code = person_salary_info[0]._code
                if code:
                    idno, tel = self.find_idno_by_code(code, pre_all_persons)
        return idno, tel

    def find_idno_by_code(self, code, texes):
        for tex_depart, datas_by_tex_depart in texes.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                if code in datas_by_depart:
                    return datas_by_depart[code]._idno, datas_by_depart[code]._tel
        return "", ""


class PersonChangeInfo(object):

    def __init__(self, period, depart_str, code, idno, name, full_departname, changeinfo, tel):
        self._period = period
        self._depart_str = depart_str
        self._code = code
        self._name = name
        self._full_departname = full_departname
        self._idno = idno
        self._tel = tel
        self._changeinfo = changeinfo

    def __str__(self):
        return '人员变化信息: 变化类别 {} - 职工编码 {} -期间 {} - 公司 {}'.format(self._changeinfo, self._code, self._period, self._depart_str)
