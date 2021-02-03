#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   attendance_operator.py
@Time    :   2021/02/03 14:12:56
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import exists
from os import makedirs
from shutil import rmtree

import xlwt

from salary_support_tools.bonus_tpl_engine import BonusInfo


class BonusOperator(object):

    def __init__(self, period, infos, columndefs):
        self._period = period  # 期限
        self._bonus_infos = infos  # 奖金数据 按照单位和部门分组完毕
        self._folder_path = r'd:\薪酬审核文件夹'
        self._columndefs = columndefs
        self._folder_name = ""  # 清理得文件目录名

    def export(self):
        """
        分组导出考勤模板 暂时按照部门导出
        """
        for depart_str, depart_infos in self._bonus_infos.items():
            for depart_depart_str, vs in depart_infos.items():
                self.to_excel(depart_str, depart_depart_str,
                              vs, self._columndefs)

    def clear_path(self):
        path = r'{}\{}\{}\{}\{}'.format(
            self._folder_path, self._period, "考勤奖金模板", "导出文件", "奖金模板")
        if exists(path):
            rmtree(path)

    def to_excel(self, companyname, departname, datas, columndefs):
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet0')
        # 写入标题
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                s.write(
                    i + 1, j, getattr(v, propertyName, 0))
        path = r'{}\{}\{}\{}\{}\{}'.format(
            self._folder_path, self._period, "考勤奖金模板", "导出文件", "奖金模板", companyname)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}_{}_{}'.format(
            path, departname, self._period, "奖金模板.xls"))
