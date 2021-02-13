#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   runner.py
@Time    :   2021/01/19 10:29:33
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import exists
from os import remove
from shutil import rmtree


from salary_support_tools.person_engine import PersonEngine
from salary_support_tools.person_salary_engine import PersonSalaryEngine
from salary_support_tools.tex_engine import TexEngine
from salary_support_tools.salary_bank_engine import SalaryBankEngine
from salary_support_tools.salary_gz_engine import SalaryGzEngine
from salary_support_tools.salary_jj_engine import SalaryJjEngine
from salary_support_tools.person_job_engine import PersonJonEngine
from salary_support_tools.salary_report_operator import SalaryReportOperator
from salary_support_tools.person_compare_engine import PersonCompareEngine
from salary_support_tools.person_compare_operator import PersonCompareOperator


class PersonCompareRunner(object):

    def __init__(self, period, departs):
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def run(self):

        # 当期人员信息
        current_p_engine = PersonEngine(self._period, self._departs)
        current_persons = current_p_engine.load_data_new()

        # 上期相关信息

        pre_period = self.pre_period()

        p_engine = PersonEngine(pre_period, self._departs)
        persons = p_engine.load_data()

        # 解析银行卡信息数据

        banks_engine = SalaryBankEngine(
            pre_period, self._departs)
        banks = banks_engine.load_data()

        jobs_engine = PersonJonEngine(
            self._period, self._departs)
        jobs = jobs_engine.load_data()

        # 载入工资信息
        gz_engine = SalaryGzEngine(pre_period)
        gz_datas = gz_engine.batch_load_data(self._departs)

        # 载入奖金信息
        jj_engine = SalaryJjEngine(pre_period)
        jj_datas = jj_engine.batch_load_data(self._departs)

        # 完成 信息 汇总 及 错误检查 输出审核结果
        merge_engine = PersonSalaryEngine(
            pre_period, persons, gz_datas, jj_datas, banks, jobs)
        err_msgs, datas, sap_datas, datas_idno = merge_engine.start()

        person_compare_engine = PersonCompareEngine(
            self._period, self._departs, current_persons, datas)
        incs, reds = person_compare_engine.start()

        person_compare_op = PersonCompareOperator(self._period, incs, reds)
        person_compare_op.export()

    def pre_period(self):
        month = 0
        year = 0
        try:
            month = int(self._period[4:])
            year = int(self._period[:4])
        except ValueError:
            raise("获取上期期间数据错误{}".format(self._period))
        if month == 1 or month > 12:
            month = 12
            year -= 1
        else:
            month -= 1
        return "{:0>4d}{:0>2d}".format(year, month)
