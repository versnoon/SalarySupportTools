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
        personInfo.period = "202001"
        columns = personInfo.getColumnDef()
        assert len(columns) > 0
        assert columns['_code'] == "工号"
        with pytest.raises(KeyError):
            columns['code']
        assert r'd:\薪酬审核文件夹\202001\人员信息.xls' == personInfo.get_exl_tpl_folder_path()

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
        personInfo.period = "2021年01月"
        columns = personInfo.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.PersonInfo, columns, personInfo.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_salaryGz_exl_to_clazz(self):
        salaryGz = ehr_engine.SalaryGzInfo()
        salaryGz.period = "2021年01月"
        salaryGz.depart = "01_集团机关"
        columns = salaryGz.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryGzInfo, columns, salaryGz.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_salaryJj_exl_to_clazz(self):
        salaryJjInfo = ehr_engine.SalaryJjInfo()
        salaryJjInfo.period = "2021年01月"
        salaryJjInfo.depart = "01_集团机关"
        columns = salaryJjInfo.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryJjInfo, columns, salaryJjInfo.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_val_bank_purpost(self):
        salaryBankInfo = ehr_engine.SalaryBankInfo()
        assert salaryBankInfo.val_bank_purpost(" 工资卡  报支卡", "工资卡") == True
        assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "工资卡") == True
        assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "奖金卡") == True
        assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "其他卡") == False
        assert salaryBankInfo.is_jj_bankno("奖金卡  工资卡  报支卡") == True
        assert salaryBankInfo.is_gz_bankno("奖金卡  工资卡  报支卡") == True
        assert salaryBankInfo.is_jj_bankno("工资卡  报支卡") == False
        assert salaryBankInfo.is_gz_bankno("报支卡") == False

    def test_salaryBank_exl_to_clazz(self):
        salaryBankInfo = ehr_engine.SalaryBankInfo()
        salaryBankInfo.period = "2021年01月"
        salaryBankInfo.depart = "01_集团机关"
        columns = salaryBankInfo.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryBankInfo, columns, salaryBankInfo.get_exl_tpl_folder_path())

        assert len(cov.loadTemp()) > 0

    def test_to_auditor(self):
        personinfo = ehr_engine.PersonInfo()
        personinfo._code = 'M73677'
        personinfo._name = '童坦'
        salarygz = ehr_engine.SalaryGzInfo()
        salarygz._gwgz = 4000
        salaryjj = ehr_engine.SalaryJjInfo()
        salaryjj._code = 'M73678'
        salaryjj._name = '其他人'
        auditor = ehr_engine.SapSalaryInfo('202101', '01')
        auditor.to_sap(personinfo, salarygz, salaryjj, None)
        assert auditor._code == 'M73677'
        assert auditor._name == '童坦'
        assert auditor._gwgz == 4000

        auditor.to_sap(None, None, salaryjj, None)
        assert auditor._code == 'M73678'
        assert auditor._name == '其他人'

        with pytest.raises(ValueError):
            auditor.to_sap(None, None, None, None)

    def test_getattr_auditor(self):
        auditor = ehr_engine.SapSalaryInfo('202101', '01')
        t = hasattr(auditor, 'period')
        v = getattr(auditor, "period", '')
        assert t == True
        assert v == '202101'

    def test_salaryPeriod_exl_to_clazz(self):
        sp = ehr_engine.SalaryPeriod()
        columns = sp.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryPeriod, columns, sp.get_exl_tpl_folder_path())
        sps = cov.loadTemp()
        assert len(sps) > 0

    def test_salaryPeriod_str(self):
        sp = ehr_engine.SalaryPeriod()
        s = sp.get_period_str(2020, 1)
        assert '2020年01月' == s
        s = sp.get_period_str(2020, 10)
        assert '2020年10月' == s

    def test_salaryDepart_exl_to_clazz(self):
        sd = ehr_engine.SalaryDepart()
        columns = sd.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryDepart, columns, sd.get_exl_tpl_folder_path())
        sps = cov.loadTemp()
        assert len(sps) > 0

    def test_salaryDepart_to_map(self):
        sd = ehr_engine.SalaryDepart()
        columns = sd.getColumnDef()
        cov = ehr_engine.ExlToClazz(
            ehr_engine.SalaryDepart, columns, sd.get_exl_tpl_folder_path())
        sps = cov.loadTemp()
        m = sd.to_map(sps)
        assert m['01'].name == "集团机关"
        with pytest.raises(KeyError):
            m['99']
