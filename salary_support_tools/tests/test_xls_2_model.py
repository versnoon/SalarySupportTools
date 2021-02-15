#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_ehr_engine.py
@Time    :   2021/01/19 15:37:35
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest


from salary_support_tools.excel.xls_2_model_util import XlsToModelUtil
from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel
from salary_support_tools.model.salary_period import SalaryPeriod


class TestXls2ModelUtil(object):
    """
    测试xls模板导入
    """

    def test_base_excel_import_model(self):
        i_model = BaseExcelImportModel(
            "gz", None, None, r'd:\审核文件夹', '工资信息', '工资信息')
        assert i_model.skip_load_with_no_file == True
        assert i_model.filepath_prefix == r'd:\审核文件夹'
        assert i_model.filename == '工资信息'

    def test_get_file_path(self):
        i_model = BaseExcelImportModel(
            "gz", None, None, r'd:\审核文件夹', '工资信息', '工资信息')
        util = XlsToModelUtil([i_model])
        file_path = util.get_tplfile_path(r'd:\审核文件夹', '工资信息', util.EXT)
        assert r'd:\审核文件夹\工资信息.xls' == file_path
        file_path = util.get_tplfile_path(r'd:\审核文件夹', '工资信息.xls')
        assert r'd:\审核文件夹\工资信息.xls' == file_path

    def test_get_model_property_name(self):
        cols = dict()
        cols["__year"] = "年"
        cols["__month"] = "月"
        i_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, r'd:\审核文件夹', 'test', '当前审核日期')
        util = XlsToModelUtil([i_model])
        yearname = util.get_model_property_name("年", cols)
        assert "__year" == yearname
        monthname = util.get_model_property_name("月", cols)
        assert "__month" == monthname
        unknow = util.get_model_property_name("unkown", cols)
        assert "" == unknow

    def cov(self, datas):
        return datas[0]

    def test_load_tpls(self):
        cols = dict()
        cols["year"] = "年"
        cols["month"] = "月"
        i_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, r'd:\薪酬审核文件夹\test', '当前审核日期', None, func=self.cov)
        util = XlsToModelUtil([i_model])
        res: dict = util.load_tpls()
        assert "sp" in res
        assert res["sp"].year == 2021
        assert res["sp"].month == 2
