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
from salary_support_tools import ehr_engine


class TestEhrEngine(object):
    """
    docstring
    """

    def test_engine_name(self, ):
        """
        docstring
        """
        engine = ehr_engine.EhrEngine()
        assert 'ehr' == engine._name

    def test_getColumnDef(self, ):
        """
        docstring
        """
        personInfo = ehr_engine.PersonInfo()
        columns = personInfo.getColumnDef()
        assert len(columns) > 0
        assert columns['_code'] == "工号"
        with pytest.raises(KeyError):
            columns['code']
        assert r'd:\薪酬审核文件夹\202101\人员信息.xls' == personInfo.get_exl_tpl_folder_path()

    def test_getPropertyName(self,):
        personInfo = ehr_engine.PersonInfo()
        columns = personInfo.getColumnDef()
        toClazz = ehr_engine.ExlToClazz(
            ehr_engine.PersonInfo, columns, personInfo.get_exl_tpl_folder_path())
        propertyName = toClazz.getPropertyName("工号")
        assert '_code' == propertyName

        errProperName = toClazz.getPropertyName("映射以外的说明")
        assert '' == errProperName

    def test_personinfo_exl_to_clazz(self):
        personInfo = ehr_engine.PersonInfo()
        columns = personInfo.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.PersonInfo, columns, personInfo.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_salaryGz_exl_to_clazz(self):
        salaryGz = ehr_engine.SalaryGzInfo()
        columns = salaryGz.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryGzInfo, columns, salaryGz.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_salaryJj_exl_to_clazz(self):
        salaryJjInfo = ehr_engine.SalaryJjInfo()
        columns = salaryJjInfo.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryJjInfo, columns, salaryJjInfo.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0
