#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_runner.py
@Time    :   2021/01/28 13:27:47
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


# from salary_support_tools import ehr_engine_two
# from salary_support_tools import person_engine
from salary_support_tools.salary_period_engine import SalaryPeriodEngine
from salary_support_tools.salary_depart_engine import SalaryDepartEngine
from salary_support_tools.person_compare_runner import PersonCompareRunner

if __name__ == "__main__":
    # engine = ehr_engine_two.EhrEngineTwo()
    # period, depart = engine.initven()
    # p_engine = person_engine.PersonEngine(period)
    # p_engine.start()

    # 载入区间信息
    # 解析审核日期
    period_engine = SalaryPeriodEngine()
    period, _ = period_engine.start()
    # 解析单位信息模板

    depart_engine = SalaryDepartEngine(period)
    departs = depart_engine.start()

    PersonCompareRunner(period, departs).run()
