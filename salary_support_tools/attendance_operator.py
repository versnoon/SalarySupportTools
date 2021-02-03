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

from salary_support_tools.attendance_tpl_engine import AttendanceInfo


class AttendanceOperator(object):

    def __init__(self, period, infos):
        self._period = period  # 期限
        self._attendance_infos = infos  # 考勤数据 按照单位和部门分组完毕
        self._folder_path = r'd:\薪酬审核文件夹'

    def export(self):
        """
        分组导出考勤模板 暂时按照部门导出
        """
        self.clear_path()
        for depart_str, depart_infos in self._attendance_infos.items():
            for depart_depart_str, vs in depart_infos.items():
                self.to_excel(depart_str, depart_depart_str, vs)

    def clear_path(self):
        path = r'{}\{}\{}\{}\{}'.format(
            self._folder_path, self._period, "考勤奖金模板", "导出文件", "考勤模板")
        if exists(path):
            rmtree(path)

    def to_excel(self, companyname, departname, datas):
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet0')
        # 写入标题
        columndefs = AttendanceInfo().getColumnDef()
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                s.write(
                    i + 1, j, getattr(v, propertyName, 0))
        path = r'{}\{}\{}\{}\{}\{}'.format(
            self._folder_path, self._period, "考勤奖金模板", "导出文件", "考勤模板", companyname)
        # departs = departname.split("___")
        # if len(departs) > 1:
        #     for dn in departs:
        #         path = path + r'\\' + dn
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}_{}_{}'.format(
            path, departname, self._period, "考勤模板.xls"))
