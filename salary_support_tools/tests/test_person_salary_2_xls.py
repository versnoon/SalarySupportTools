#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_person_salary_2_xls.py
@Time    :   2021/02/20 15:35:55
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pytest


from salary_support_tools.excel.model_2_xls import ModelToXls
from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.salary_period import SalaryPeriod


class TestPersonSalaryToXls:

    def test_create_person_salary_to_xls_model(self):

        cols = list()
        cols.append(ExportColumn("_period", "期间"))
        datas = list()
        datas.append(TestModel("202101"))
        datas.append(TestModel("202102"))
        util = ModelToXls([BaseExcelExportModel(
            cols, datas, "导出文件夹", "测试", None, SalaryPeriod(2021, 2)), BaseExcelExportModel(
            cols, datas, "导出文件夹", "测试1", None, SalaryPeriod(2021, 2))])
        util.export()


class ExportColumn:

    def __init__(self, code, name):
        self._code = code
        self._name = name


class TestModel:

    def __init__(self, period):
        self._period = period
