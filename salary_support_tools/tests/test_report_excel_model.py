#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_report_excel_model.py
@Time    :   2021/03/18 15:06:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.report_excel_export import ReportExcelExport
from salary_support_tools.model.salary_period import SalaryPeriod


class TestReportExcelModel:

    def test_create(self):
        report_title = f"马钢（集团）控股有限公司_{SalaryPeriod(2021, 4)}_集团机关_薪酬汇总表"
        report = ReportExcelExport(report_title, dict())
        report.create_report_excel_file()
