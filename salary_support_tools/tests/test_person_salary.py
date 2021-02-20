#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_person_salary.py
@Time    :   2021/02/19 13:21:26
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.excel.xls_2_model_util import XlsToModelUtil
from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel
from salary_support_tools.model.salary_period import SalaryPeriod, SalaryPeriodConventor
from salary_support_tools.model.salary_depart import SalaryDepart, SalaryDepartConventor
from salary_support_tools.model.salary_person import SalaryPerson, SalaryPersonConventor
from salary_support_tools.model.salary_job import SalaryJob, SalaryJobConventor
from salary_support_tools.model.salary_bank import SalaryBank, SalaryBankConventor
from salary_support_tools.model.salary_gz import SalaryGz, SalaryGzConventor
from salary_support_tools.model.salary_jj import SalaryJj, SalaryJjConventor
from salary_support_tools.model.salary_tex import SalaryTex
from salary_support_tools.excel.tex_xls_2_model_util import TexXlsToModelUtil
from salary_support_tools.engine.merge_engine import MergeEngine


class TestPersonSalary:

    def prepare_data(self):
        cols = cols = SalaryPeriod.cols()
        sp_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, '当前审核日期', None, convertor=SalaryPeriodConventor())
        util = XlsToModelUtil([sp_model])
        res: dict = util.load_tpls()
        period = res["sp"]

        sd_model = BaseExcelImportModel(
            "sd", SalaryDepart, SalaryDepart.cols(), '审核机构信息', None, convertor=SalaryDepartConventor(), period=period)

        util = XlsToModelUtil([sd_model])
        res: dict = util.load_tpls()
        departs = res["sd"]

        s_p_model = BaseExcelImportModel(
            SalaryPerson.name_key, SalaryPerson, SalaryPerson.cols(), '', '人员信息', convertor=SalaryPersonConventor(), period=period, departs=departs)
        s_j_model = BaseExcelImportModel(
            SalaryJob.name_key, SalaryJob, SalaryJob.cols(), '', '岗位聘用信息', convertor=SalaryJobConventor(), period=period, departs=departs)
        s_b_model = BaseExcelImportModel(
            SalaryBank.name_key, SalaryBank, SalaryBank.cols(), '', '银行卡信息', convertor=SalaryBankConventor(), period=period, departs=departs)
        s_gz_model = BaseExcelImportModel(
            SalaryGz.name_key, SalaryGz, SalaryGz.cols(), '', '工资信息', convertor=SalaryGzConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        s_jj_model = BaseExcelImportModel(
            SalaryJj.name_key, SalaryJj, SalaryJj.cols(), '', '奖金信息', convertor=SalaryJjConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        util = XlsToModelUtil(
            [s_p_model, s_j_model, s_b_model, s_gz_model, s_jj_model])
        res: dict = util.load_tpls()

        tex_util = TexXlsToModelUtil(
            period, departs, res[SalaryPerson.name_key])
        tex_res: dict = tex_util.load_tex_tpls()

        return period, departs, res[SalaryPerson.name_key], res[SalaryJob.name_key], res[SalaryBank.name_key], res[SalaryGz.name_key], res[SalaryJj.name_key], tex_res

    def test_create_person_salary(self):
        period, departs, persons, jobs, banks, gzs, jjs, texes = self.prepare_data()
        merge_engine = MergeEngine(
            period, departs, persons, jobs, gzs, jjs, banks, texes)
        res = merge_engine.merge_salary_info()
        assert "M27108" in res["马钢（集团）控股有限公司(总部)"]["01_集团机关"]
        assert res["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M27108"]._gz is None
        assert res["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M27108"]._jj._totalPayable == 83928
