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
        datas = self.merge_salary_person_bank_info(
            self._persons, self._banks, self.merge_salary_info(self._gzs, self._jjs))
        has_err, err_msgs = self.validate(datas)
        return has_err, err_msgs, datas

    def merge_salary_info(self, gzs, jjs):
        # 根据单位分组工资奖金数据
        infos = OrderedDict()
        for gz in gzs:
            code = gz._code
            info = PersonSalaryInfo()
            info._period = self._period  # 期间信息
            info._depart = gz.depart  # 单位信息
            info._gz = gz  # 工资信息
            vs = OrderedDict()
            if info._depart in infos:
                vs = infos[info._depart]
            vs[code] = info
            infos[info._depart] = vs
        for jj in jjs:
            code = jj._code
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
        return person_salary_infos

    def get_person(self, code, persons):
        person = None
        if code in persons["c"]:  # 当前人员信息
            person = persons["c"][code]
            return person, "c"
        elif code in persons["o"]:  # 上期人员信息
            person = persons["o"][code]
            return person, "o"
        elif code in persons["o_o"]:
            person = persons["o"][code]
            return person, "o_o"
        else:
            return person, "n"

    def validate(self, person_salary_infos):
        """
        验证工资数据，验证奖金数据
        """
        # 验证工资
        #  实发 < 0
        #  缺少工资账号
        #  岗位绩效  缺少岗位工资
        #  生活费   岗位工资不为0
        err_mgs = dict()
        for depart, psis in person_salary_infos.items():
            err_message = []
            for code, person_salary_info in psis.items():
                person = person_salary_info._person
                gz = person_salary_info._gz
                jj = person_salary_info._jj
                banks = person_salary_info._banks
                if gz is not None:
                    # 实发小于0
                    if gz._pay < 0:
                        err_message.append(self.err_mss(
                            "工资信息错误", "工资实发异常：工资实发小于0，实发金额{}".format(gz._pay), person))
                    # 缺少工资银行卡号
                    if gz._pay > 0:
                        if banks is None or banks[gz] is None:
                            err_message.append(self.err_mss(
                                "银行卡信息错误", "缺少工资卡信息", person))
                    # 缺少岗位工资
                    if gz._salaryModel.startswith("岗位绩效工资制") and gz._gwgz == 0:
                        err_message.append(self.err_mss(
                            "工资信息错误", "岗位工资异常：缺少岗位工资信息", person))
                if jj is not None:
                    # 实发小于0
                    if jj._pay < 0:
                        err_message.append(self.err_mss(
                            "奖金信息错误", "奖金实发小于0，实发金额{}".format(gz._pay), person))
                    # 缺少工资银行卡号
                    if jj._pay > 0:
                        if banks is None or banks[jj] is None:
                            err_message.append(self.err_mss(
                                "银行卡信息错误", "缺少奖金卡信息", person))
            if len(err_message) > 0:
                err_mgs[depart] = err_message

        return len(err_mgs) > 0, err_mgs

        # for depart, vs in gzm.items():
        #     err_message = []
        #     for v in vs:
        #         if depart in err_mgs:
        #             err_message = err_mgs[depart]
        #         if v._pay < 0:
        #             err_message.append(self.err_mss(
        #                 persons, v._code, "工资实发异常：工资实发小于0，实发金额{}".format(v._pay)))
        #         bank = banks[depart][v._code]
        #         bankno = None
        #         if bank is not None:
        #             bankno = banks[depart][v._code]["gz"]
        #         if v._pay > 0 and (bankno is None or bankno._bankNo is None or bankno._bankNo == ""):
        #             err_message.append(self.err_mss(
        #                 persons, v._code, "银行卡信息异常：缺少工资卡信息"))
        #         if v._salaryModel.startswith("岗位绩效工资制") and v._gwgz == 0:
        #             err_message.append(self.err_mss(
        #                 persons, v._code, "岗位工资异常：缺少岗位工资信息"))
        #         # if v._salaryModel.startswith("生活费") and v._shf != v._totalPayable:
        #         #     err_message.append(self.err_mss(
        #         #         persons, v._code, "生活费人员工资异常：其他工资{}不等于应发合计{}".format(v._shf, v._totalPayable)))
        #     if len(err_message) > 0:
        #         err_mgs[depart] = err_message
        # # 验证奖金
        # # 实发  < 0
        # # 缺少哦奖金账号
        # for depart, vs in jjm.items():
        #     err_message = []
        #     for v in vs:
        #         if depart in err_mgs:
        #             err_message = err_mgs[depart]
        #         if v._pay < 0:
        #             err_message.append(self.err_mss(
        #                 persons, v._code, "奖金实发异常：奖金实发小于0，实发金额{}".format(v._pay)))
        #         bank = banks[depart][v._code]
        #         bankno = None
        #         if bank is not None:
        #             bankno = banks[depart][v._code]["jj"]
        #         if v._pay > 0 and (bankno is None or bankno._bankNo is None or bankno._bankNo == ""):
        #             err_message.append(self.err_mss(
        #                 persons, v._code, "银行卡信息异常：缺少奖金卡信息"))
        #     if len(err_message) > 0:
        #         err_mgs[depart] = err_message
        # return err_mgs

    def err_mss(self, err_type, message, person) -> str:
        if person is not None:
            return '错误信息提示:  ->  错误类型 {} - 错误信息 {} - 错误人员 {}'.format(err_type, message, person)
        return '错误信息提示:  ->  错误类型 {} - 错误信息 {}'.format(err_type, message)


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
