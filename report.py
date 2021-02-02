#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report.py
@Time    :   2021/02/02 17:14:11
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools import salary_period_engine
from salary_support_tools import salary_depart_engine
from salary_support_tools.report_runner import ReportRunner

if __name__ == "__main__":

    # 载入区间信息
    # 解析审核日期
    period_engine = salary_period_engine.SalaryPeriodEngine()
    period, _ = period_engine.start()
    # 解析单位信息模板

    depart_engine = salary_depart_engine.SalaryDepartEngine(period)
    departs = depart_engine.start()

    ReportRunner(period, departs).run()
