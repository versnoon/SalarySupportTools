#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   load_tpls_engine.py
@Time    :   2021/02/25 12:49:31
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.excel.model_2_xls import ModelToXls
from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.export.gz_export_model import GzExport
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
from salary_support_tools.excel.xls_2_model_util import XlsToModelUtil
from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel


class LoadTplEngine:
    """
    加载模板数据
    """

    def load_current_period_departs(self):
        sp_model = BaseExcelImportModel(
            "sp", SalaryPeriod, SalaryPeriod.cols(), '当前审核日期', None, convertor=SalaryPeriodConventor())
        util = XlsToModelUtil([sp_model])
        res: dict = util.load_tpls()
        period = res["sp"]

        sd_model = BaseExcelImportModel(
            "sd", SalaryDepart, SalaryDepart.cols(), '审核机构信息', None, convertor=SalaryDepartConventor(), period=period)

        util = XlsToModelUtil([sd_model])
        res: dict = util.load_tpls()
        departs = res["sd"]

        return period, departs

    def pre_period(self, period: SalaryPeriod):
        month = period.month
        year = period.year
        if month == 1 or month > 12:
            month = 12
            year -= 1
        else:
            month -= 1
        return SalaryPeriod(year, month)

    def load_persons(self, period: SalaryPeriod, departs):
        s_p_model = BaseExcelImportModel(
            SalaryPerson.name_key, SalaryPerson, SalaryPerson.cols(), '', '人员信息', convertor=SalaryPersonConventor(), period=period, departs=departs)
        util = XlsToModelUtil(
            [s_p_model])
        res: dict = util.load_tpls()

        return res[SalaryPerson.name_key]

    def load_tpl_by_period(self, period: SalaryPeriod):
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
            period, departs, res[SalaryPerson.name_key], res[SalaryGz.name_key], res[SalaryJj.name_key])
        texes: dict = tex_util.load_tex_tpls()

        persons = res[SalaryPerson.name_key]
        jobs = res[SalaryJob.name_key]
        gzs = res[SalaryGz.name_key]
        jjs = res[SalaryJj.name_key]
        banks = res[SalaryBank.name_key]

        m_engine = MergeEngine(period, departs, persons,
                               jobs, gzs, jjs, banks, texes)
        merge_infos = m_engine.merge_salary_info()
        return period, departs, persons, jobs, gzs, jjs, banks, texes, merge_infos
