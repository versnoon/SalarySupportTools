#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_operator.py
@Time    :   2021/02/04 16:05:48
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import exists
from os import makedirs

import xlwt

from salary_support_tools.person_compare_engine import PersonCompareEngine


class PersonCompareOperator(object):

    def __init__(self, period, incs, redus):
        self._period = period  # 期限
        self._incs = incs  # 增员信息
        self._redus = redus  # 减员信息
        self._folder_path = r'd:\薪酬审核文件夹'

    def export(self):
        for depart_str, infos in self._incs.items():
            self.export_change_excel("增员信息", depart_str, infos)
        for depart_str, infos in self._redus.items():
            self.export_change_excel("减员信息", depart_str, infos)

    def export_change_excel(self, filename, depart, datas):

        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet1')

        columndefs = PersonCompareEngine().columns_def()
        # 写入标题
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                try:
                    s.write(
                        i+1, j, getattr(v, propertyName, 0))
                except TypeError:
                    pass

            path = r'{}\{}\{}'.format(
                self._folder_path, self._period, "人员变化情况")
            if not exists(path):
                makedirs(path)
            b.save(r'{}\{}_{}_{}{}'.format(
                path, depart, self._period, filename, ".xls"))
