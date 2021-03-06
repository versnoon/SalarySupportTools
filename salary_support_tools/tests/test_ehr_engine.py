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
# from salary_support_tools import ehr_engine


class TestEhrEngine(object):
    """
    docstring
    """

    # def test_engine_name(self, ):
    #     """
    #     docstring
    #     """
    #     engine = ehr_engine.EhrEngine()
    #     assert 'ehr' == engine._name

    # def test_getColumnDef(self, ):
    #     """
    #     docstring
    #     """
    #     personInfo = ehr_engine.PersonInfo()
    #     personInfo.period = "202001"
    #     columns = personInfo.getColumnDef()
    #     assert len(columns) > 0
    #     assert columns['_code'] == "工号"
    #     with pytest.raises(KeyError):
    #         columns['code']
    #     assert r'd:\薪酬审核文件夹\202001\人员信息.xls' == personInfo.get_exl_tpl_folder_path()

    # def test_getPropertyName(self,):
    #     personInfo = ehr_engine.PersonInfo()
    #     columns = personInfo.getColumnDef()
    #     toClazz = ehr_engine.ExlToClazz(
    #         ehr_engine.PersonInfo, columns, personInfo.get_exl_tpl_folder_path())
    #     propertyName = toClazz.getPropertyName("工号")
    #     assert '_code' == propertyName

    #     errProperName = toClazz.getPropertyName("映射以外的说明")
    #     assert '' == errProperName

    # def test_personinfo_exl_to_clazz(self):
    #     personInfo = ehr_engine.PersonInfo()
    #     personInfo.period = "2021年01月"
    #     columns = personInfo.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.PersonInfo, columns, personInfo.get_exl_tpl_folder_path())

    #     assert len(cov.loadTemp()) > 0

    # def test_salaryGz_exl_to_clazz(self):
    #     salaryGz = ehr_engine.SalaryGzInfo()
    #     salaryGz.period = "2021年01月"
    #     salaryGz.depart = "01_集团机关"
    #     columns = salaryGz.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.SalaryGzInfo, columns, salaryGz.get_exl_tpl_folder_path())

    #     assert len(cov.loadTemp()) > 0

    # def test_salaryJj_exl_to_clazz(self):
    #     salaryJjInfo = ehr_engine.SalaryJjInfo()
    #     salaryJjInfo.period = "2021年01月"
    #     salaryJjInfo.depart = "01_集团机关"
    #     columns = salaryJjInfo.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.SalaryJjInfo, columns, salaryJjInfo.get_exl_tpl_folder_path())

    #     assert len(cov.loadTemp()) > 0

    # def test_val_bank_purpost(self):
    #     salaryBankInfo = ehr_engine.SalaryBankInfo()
    #     assert salaryBankInfo.val_bank_purpost(" 工资卡  报支卡", "工资卡") == True
    #     assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "工资卡") == True
    #     assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "奖金卡") == True
    #     assert salaryBankInfo.val_bank_purpost("奖金卡  工资卡  报支卡", "其他卡") == False
    #     assert salaryBankInfo.is_jj_bankno("奖金卡  工资卡  报支卡") == True
    #     assert salaryBankInfo.is_gz_bankno("奖金卡  工资卡  报支卡") == True
    #     assert salaryBankInfo.is_jj_bankno("工资卡  报支卡") == False
    #     assert salaryBankInfo.is_gz_bankno("报支卡") == False

    # def test_salaryBank_exl_to_clazz(self):
    #     salaryBankInfo = ehr_engine.SalaryBankInfo()
    #     salaryBankInfo.period = "2021年01月"
    #     salaryBankInfo.depart = "01_集团机关"
    #     columns = salaryBankInfo.getColumnDef()
    #     cov = ehr_engine.ExlsToClazz(
    #         ehr_engine.SalaryBankInfo, columns, salaryBankInfo.get_exl_tpl_folder_path_prefix(), salaryBankInfo.get_exl_tpl_file_name_prefix())

    #     assert len(cov.loadTemp()) > 0

    # def test_to_auditor(self):
    #     personinfo = ehr_engine.PersonInfo()
    #     personinfo._code = 'M73677'
    #     personinfo._name = '童坦'
    #     salarygz = ehr_engine.SalaryGzInfo()
    #     salarygz._gwgz = 4000
    #     salaryjj = ehr_engine.SalaryJjInfo()
    #     salaryjj._code = 'M73678'
    #     salaryjj._name = '其他人'
    #     auditor = ehr_engine.SapSalaryInfo('202101', '01')
    #     auditor.to_sap(personinfo, salarygz, salaryjj, None)
    #     assert auditor._code == 'M73677'
    #     assert auditor._name == '童坦'
    #     assert auditor._gwgz == 4000

    #     auditor.to_sap(None, None, salaryjj, None)
    #     assert auditor._code == 'M73678'
    #     assert auditor._name == '其他人'

    #     with pytest.raises(ValueError):
    #         auditor.to_sap(None, None, None, None)

    # def test_getattr_auditor(self):
    #     auditor = ehr_engine.SapSalaryInfo('202101', '01')
    #     t = hasattr(auditor, 'period')
    #     v = getattr(auditor, "period", '')
    #     assert t == True
    #     assert v == '202101'

    # def test_salaryPeriod_exl_to_clazz(self):
    #     sp = ehr_engine.SalaryPeriod()
    #     columns = sp.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.SalaryPeriod, columns, sp.get_exl_tpl_folder_path())
    #     sps = cov.loadTemp()
    #     assert len(sps) > 0

    # def test_salaryPeriod_str(self):
    #     sp = ehr_engine.SalaryPeriod()
    #     s = sp.get_period_str(2020, 1)
    #     assert '2020年01月' == s
    #     s = sp.get_period_str(2020, 10)
    #     assert '2020年10月' == s

    # def test_salaryDepart_exl_to_clazz(self):
    #     sd = ehr_engine.SalaryDepart()
    #     columns = sd.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.SalaryDepart, columns, sd.get_exl_tpl_folder_path())
    #     sps = cov.loadTemp()
    #     assert len(sps) > 0

    # def test_salaryDepart_to_map(self):
    #     sd = ehr_engine.SalaryDepart()
    #     columns = sd.getColumnDef()
    #     cov = ehr_engine.ExlToClazz(
    #         ehr_engine.SalaryDepart, columns, sd.get_exl_tpl_folder_path())
    #     sps = cov.loadTemp()
    #     m = sd.to_map(sps)
    #     assert m['01'].name == "集团机关"
    #     assert m["01"].get_departs()[0] == "办公室（党委办公室）"
    #     with pytest.raises(KeyError):
    #         m['99']

    # def test_salaryJjInfo_to_sum(self):
    #     jj = ehr_engine.SalaryJjInfo()
    #     jj._bonusOne = 1000
    #     jj2 = ehr_engine.SalaryJjInfo()
    #     jj2._bonusOne = 2000
    #     jj2._bonusTwo = 4000
    #     jj.to_sum(jj2)
    #     assert jj._bonusOne == 3000
    #     assert jj._bonusTwo == 4000

    # def test_salaryJjInfo_to_map(self):
    #     jj = ehr_engine.SalaryJjInfo()
    #     jj.period = "2021年01月"
    #     jj.depart = "01_集团机关"
    #     columns = jj.getColumnDef()
    #     cov = ehr_engine.ExlsToClazz(
    #         ehr_engine.SalaryJjInfo, columns, jj.get_exl_tpl_folder_path_prefix(), jj.get_exl_tpl_file_name_prefix(), 0, True)
    #     jjs = cov.loadTemp()
    #     m = jj.to_map(jjs)
    #     assert m['M58709']._jbjj == 3252 * 1

    # def test_salaryBankInfo_to_map(self):
    #     bank = ehr_engine.SalaryBankInfo()
    #     bank.period = "2021年01月"
    #     columns = bank.getColumnDef()
    #     cov = ehr_engine.ExlsToClazz(
    #         ehr_engine.SalaryBankInfo, columns, bank.get_exl_tpl_folder_path_prefix(), bank.get_exl_tpl_file_name_prefix(), 0, True)
    #     banks = cov.loadTemp()
    #     m = bank.to_map(banks)
    #     assert 'M73677' in m
    #     assert 'M58100' in m

    # def test_salaryDepart_get_departs(self):
    #     salaryDepart = ehr_engine.SalaryDepart()
    #     salaryDepart.name = "集团机关"
    #     salaryDepart.salaryScope = "01"
    #     salaryDepart.sortno = 1
    #     salaryDepart.relativeUnits = "办公室（党委办公室）|党委工作部（党委组织部、人力资源部）|纪委（审计稽查部）|工会|投资管理部（法律事务部）|财务部|管理创新部、科技管理部|人力资源服务中心|宝武运营共享服务中心马鞍山区域分中心|行政事务中心"
    #     departs = salaryDepart.get_departs()
    #     assert departs[0] == "办公室（党委办公室）"
    #     assert departs[1] == "党委工作部（党委组织部、人力资源部）"
    #     salaryDepart.relativeUnits = ""
    #     departs = salaryDepart.get_departs()
    #     assert departs[0] == "集团机关"

    # def test_get_departLevelTow(self):
    #     jj = ehr_engine.SalaryJjInfo()
    #     jj._departfullinfo = "马钢（集团）控股有限公司(总部)\宝武运营共享服务中心马鞍山区域分中心\采购核算组"
    #     d = jj._get_departLevelTow()
    #     assert d == "宝武运营共享服务中心马鞍山区域分中心"
    #     jj._departfullinfo = "马钢（集团）控股有限公司(总部)"
    #     with pytest.raises(ValueError):
    #         jj._get_departLevelTow()
    #     jj._departfullinfo = "马钢（集团）控股有限公司(总部)\财务部"
    #     d = jj._get_departLevelTow()
    #     assert d == "财务部"
