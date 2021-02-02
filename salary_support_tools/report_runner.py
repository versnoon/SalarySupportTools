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
from salary_support_tools.salary_report_operator import SalaryReportOperator


class ReportRunner(object):

    def __init__(self, period, departs):
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def run(self):

        p_engine = PersonEngine(self._period)
        persons = p_engine.load_data()
        # 解析银行卡信息数据

        banks_engine = SalaryBankEngine(
            self._period, self._departs)
        banks = banks_engine.load_data()

        # 载入工资信息
        gz_engine = SalaryGzEngine(self._period)
        gz_datas = gz_engine.batch_load_data(self._departs)

        # 载入奖金信息
        jj_engine = SalaryJjEngine(self._period)
        jj_datas = jj_engine.batch_load_data(self._departs)

        # 完成 信息 汇总 及 错误检查 输出审核结果
        merge_engine = PersonSalaryEngine(
            self._period, persons, gz_datas, jj_datas, banks)
        err_msgs, datas, sap_datas, datas_idno = merge_engine.start()

        # 输出

        # 工资奖金文件输出
        report_op = SalaryReportOperator(
            self._period, self._departs, gz_datas, jj_datas, datas, sap_datas, err_msgs)
        report_op._exportable = True
        report_op.export()
