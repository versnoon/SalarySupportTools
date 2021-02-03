#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_attendance_tpl_engine.py
@Time    :   2021/02/03 13:00:04
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pytest


from salary_support_tools.attendance_tpl_engine import AttendanceTplEngine, AttendanceInfo
from salary_support_tools.salary_depart_engine import SalaryDepart


class TestAttendacntTplEngine(object):
    """
    考勤模板加载模块相关测试
    """

    def test_engine_name(self):
        engine = AttendanceTplEngine("", None)
        assert engine._name == "attendance_tpl_op"

    def test_load_data(self):
        engine = AttendanceTplEngine("202101", None)
        assert len(engine.load_data()) > 0

    def test_split_depart_fullname(self):
        info = AttendanceInfo()
        info._depart_fullname = r"马鞍山钢铁股份有限公司（总部）\检测中心1\产成品单元1\成品检验三作业区1\成品检验三作业区低倍高铣组"
        assert "马鞍山钢铁股份有限公司（总部）" == info.split_depart_fullname(0)
        assert "检测中心1" == info.split_depart_fullname(1)
        assert "产成品单元1" == info.split_depart_fullname(2)
        assert "成品检验三作业区1" == info.split_depart_fullname(3)
        assert "成品检验三作业区低倍高铣组" == info.split_depart_fullname(4)
        assert "成品检验三作业区低倍高铣组" == info.split_depart_fullname(5)

    def test_company_name(self):
        info = AttendanceInfo()
        info._depart_fullname = r"马鞍山钢铁股份有限公司（总部）\检测中心1\产成品单元1\成品检验三作业区1\成品检验三作业区低倍高铣组"
        assert "检测中心1" == info.company_name()

    def test_depart_name(self):
        info = AttendanceInfo()
        info._depart_fullname = r"马鞍山钢铁股份有限公司（总部）\检测中心1\产成品单元1\成品检验三作业区1\成品检验三作业区低倍高铣组"
        assert "产成品单元1" == info.depart_name()

    def test_group_by_depart_info(self):
        info = AttendanceInfo()
        info._code = "M"
        info._depart_fullname = r"马鞍山钢铁股份有限公司（总部）\检测中心1\产成品单元1\成品检验三作业区1\成品检验三作业区低倍高铣组"
        departs = dict()
        depart = SalaryDepart()
        depart.name = "检测中心1"
        depart.salaryScope = "1"
        departs["1"] = depart
        engine = AttendanceTplEngine("2021", departs)
        res = dict()
        engine.group_by_depart_info(info, res)
        assert "1_检测中心1" in res
        assert res["1_检测中心1"]["产成品单元1"] is not None
