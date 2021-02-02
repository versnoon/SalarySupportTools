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
from salary_support_tools.tex_operator import TexExport
from salary_support_tools.salary_operator import SalaryOperator


class AuditorRunner(object):

    def __init__(self, period, departs):
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def run(self):

        self.clearPath()

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

        # 验证当期所得税
        tex_engine = TexEngine(self._period, datas, datas_idno, self._departs)
        tex_err_msgs, tex_datas = tex_engine.start()

        # 输出

        # 工资奖金文件输出
        salary_op = SalaryOperator(
            self._period, self._departs, gz_datas, jj_datas, datas, sap_datas, err_msgs)
        salary_op._exportable = True
        salary_op.export()
        # 税务相关文件输出
        tex_op = TexExport(
            self._period, sap_datas, tex_datas, tex_err_msgs)
        tex_op._exportable = True
        tex_op.export()

    def clearPath(self):
        for depart in self._departs.values():
            depart_folder_name = depart.get_depart_salaryScope_and_name()
            path_prefix = r"{}\{}\{}".format(
                self._folder_path, self._period, depart_folder_name)
            self.clear_file(path_prefix, "工资信息.xls")
            self.clear_file(path_prefix, "奖金信息.xls")
            self.clear_file(path_prefix, "错误信息.txt")
            self.clear_file(path_prefix, "个税核对结果.txt")
            self.clear_folder(path_prefix, "导出文件")

    def clear_file(self, path_prefix, filename):
        """
        删除文件
        """
        file_path = r'{}\{}'.format(path_prefix, filename)
        if exists(file_path):
            remove(file_path)

    def clear_folder(self, path_prefix, foldername):
        """
        删除文件见
        """
        folder_path = r'{}\{}'.format(path_prefix, foldername)
        if exists(folder_path):
            rmtree(folder_path)
