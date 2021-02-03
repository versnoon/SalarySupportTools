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
from salary_support_tools.bonus_tpl_engine import BonusTplEngine, BonusInfo
from salary_support_tools.bonus_operator import BonusOperator


class AttendanceBonusTplRunner(object):

    def __init__(self, period, departs):
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def run(self):

        # 考勤文件分割
        att_engine = AttendanceTplEngine(self._period, self._departs)
        att_datas = att_engine.start()

        att_op = AttendanceOperator(self._period, att_datas)
        att_op.export()

        # 奖金文件分割
        bonus_engine = BonusTplEngine(self._period, self._departs)
        jt_datas, jp_datas, xw_datas, lt_datas, bwb_datas, gf_datas = bonus_engine.start()
        bonus = BonusInfo()
        jt_op = BonusOperator(self._period, jt_datas, bonus.get_jt_columns())
        # 清理文件夹
        jt_op.clear_path()
        jt_op.export()
        jp_op = BonusOperator(self._period, jp_datas, bonus.get_jp_columns())
        jp_op.export()
        xw_op = BonusOperator(self._period, xw_datas, bonus.get_xw_columns())
        xw_op.export()
        lt_op = BonusOperator(self._period, lt_datas, bonus.get_lt_columns())
        lt_op.export()
        bw_op = BonusOperator(self._period, bwb_datas, bonus.get_bwb_columns())
        bw_op.export()
        gf_op = BonusOperator(self._period, gf_datas, bonus.get_gf_columns())
        gf_op.export()
