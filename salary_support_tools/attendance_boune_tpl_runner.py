#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   attendance_boune_tpl_runner.py
@Time    :   2021/02/03 14:25:59
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.attendance_tpl_engine import AttendanceTplEngine
from salary_support_tools.attendance_operator import AttendanceOperator


class AttendanceBouneTplRunner(object):

    def __init__(self, period, departs):
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def run(self):
        engine = AttendanceTplEngine(self._period, self._departs)
        datas = engine.start()

        op = AttendanceOperator(self._period, datas)
        op.export()
