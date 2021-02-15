#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary_period_model.py
@Time    :   2021/02/13 11:55:07
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest

from salary_support_tools.model.salary_depart import SalaryDepart


class TestSalaryDepart(object):

    def test_create_salary_period(self):
        model = SalaryDepart()
        model.salaryScope = "01"  # 工资范围
        model.name = "集团机关"  # 单位名称
        model.sortno = 1  # 显示顺序
        model.relativeUnits = "办公室（党委办公室）|党委工作部（党委组织部、人力资源部）|纪委（审计稽查部）|工会|投资管理部（法律事务部）|财务部|管理创新部、科技管理部|人力资源服务中心|宝武运营共享服务中心马鞍山区域分中心|行政事务中心|马钢集团安全生产管理部|马钢集团法律事务部|马钢集团规划与科技部|马钢集团技术改造部|马钢集团精益办|马钢集团经营财务部|马钢集团能源环保部|马钢集团人力资源部|马钢集团运营改善部"  # 相关单位
        model.status = "1"  # 审核状态 不为空 及做数据的输出和导出 空不做动作
        model.texdepart = "马钢（集团）控股有限公司(总部)"  # "税务机构"
        assert len(model.get_departs()) > 0
        assert model.get_departs()[0] == '办公室（党委办公室）'
        assert model.contain_relativeunits() == True
        assert '01_集团机关' == model.get_depart_salaryScope_and_name()
        assert True == model.is_depart("集团机关")
        assert True == model.is_depart("工会")
        assert False == model.is_depart("工会1")
        assert False == model.need_audit()
        model.relativeUnits = ""
        assert False == model.contain_relativeunits()
        model.status = None
        assert True == model.need_audit()
        model.status = ""
        assert True == model.need_audit()
