#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_period_engine.py
@Time    :   2021/01/28 15:47:31
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import exists
from os import makedirs

from salary_support_tools.exl_to_clazz import ExlToClazz


class SalaryPeriodEngine(object):
    def __init__(self):
        self.name = "salary_period"
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        sps = self.load_data()
        if len(sps) != 1:
            raise ValueError("审核日期模板解析错误,请检查'当前审核日期.xls'模板")
        period = self.get_period_str(sps[0].year, sps[0].month)
        # 初始化日期文件夹 工作目录
        current_folder_path = r"{}\{}".format(self._folder_prefix, period)
        if not exists(current_folder_path):
            makedirs(current_folder_path)
        return period, sps[0]

    def load_data(self):
        salaryPeriod = SalaryPeriod()
        sp = ExlToClazz(SalaryPeriod, salaryPeriod.getColumnDef(),
                        salaryPeriod.get_exl_tpl_folder_path())
        return sp.loadTemp()

    def get_period_str(self, year, month):
        return "{:0>4d}{:0>2d}".format(int(year), int(month))


class SalaryPeriod(object):

    def __init__(self):
        self.year: int = 0
        self.month: int = 0

    def __str__(self):
        return '审核日期信息: 年 {} - 月 {}'.format(self.year, self.month)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["year"] = "年"
        columns["month"] = "月"

        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\当前审核日期.xls'
