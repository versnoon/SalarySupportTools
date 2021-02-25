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
from salary_support_tools.model.salary_period import SalaryPeriod, SalaryPeriodConventor
from salary_support_tools.model.salary_depart import SalaryDepart, SalaryDepartConventor
from salary_support_tools.model.salary_person import SalaryPerson, SalaryPersonConventor
from salary_support_tools.model.salary_job import SalaryJob, SalaryJobConventor
from salary_support_tools.model.salary_bank import SalaryBank, SalaryBankConventor
from salary_support_tools.model.salary_gz import SalaryGz, SalaryGzConventor
from salary_support_tools.model.salary_jj import SalaryJj, SalaryJjConventor
from salary_support_tools.model.salary_tex import SalaryTex
from salary_support_tools.model.salary_attendance import SalaryAttendance, SalaryAttendanceConventor
from salary_support_tools.model.salary_bonus import SalaryBonus, SalaryBonusConventor
from salary_support_tools.excel.tex_xls_2_model_util import TexXlsToModelUtil


class TestXls2ModelUtil(object):
    """
    测试xls模板导入
    """

    def test_base_excel_import_model(self):
        i_model = BaseExcelImportModel(
            "gz", None, None, '工资信息', '工资信息')
        assert i_model.skip_load_with_no_file == True
        assert i_model.filename == '工资信息'

    def test_get_file_path(self):
        i_model = BaseExcelImportModel(
            "gz", None, None,  '工资信息', '工资信息')
        util = XlsToModelUtil([i_model])
        file_path = util.get_tplfile_path(r'd:\薪酬审核文件夹', '工资信息', util.EXT)
        assert r'd:\薪酬审核文件夹\工资信息.xls' == file_path
        file_path = util.get_tplfile_path(r'd:\薪酬审核文件夹', '工资信息.xls')
        assert r'd:\薪酬审核文件夹\工资信息.xls' == file_path

    def test_get_model_property_name(self):
        cols = SalaryPeriod.cols()
        i_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, r'd:\审核文件夹', 'test', '当前审核日期')
        util = XlsToModelUtil([i_model])
        yearname = util.get_model_property_name("年", cols)
        assert "year" == yearname
        monthname = util.get_model_property_name("月", cols)
        assert "month" == monthname
        unknow = util.get_model_property_name("unkown", cols)
        assert "" == unknow

    def test_load_tpls(self):
        cols = cols = SalaryPeriod.cols()
        sp_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, '当前审核日期', None, convertor=SalaryPeriodConventor())
        util = XlsToModelUtil([sp_model])
        res: dict = util.load_tpls()
        assert "sp" in res
        assert res["sp"].year == 2021
        assert res["sp"].month == 2
        period = res["sp"]

        sd_model = BaseExcelImportModel(
            "sd", SalaryDepart, SalaryDepart.cols(), '审核机构信息', None, convertor=SalaryDepartConventor(), period=period)

        util = XlsToModelUtil([sd_model])
        res: dict = util.load_tpls()
        assert '202102' == sd_model.period.period
        assert "sd" in res
        assert len(res["sd"]) > 0
        assert "01" in res["sd"]
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
        s_a_model = BaseExcelImportModel(
            SalaryAttendance.name_key, SalaryAttendance, SalaryAttendance.cols(), '', '考勤模板', convertor=SalaryAttendanceConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_jt_model = BaseExcelImportModel(
            SalaryBonus.NAME_JT, SalaryBonus, SalaryBonus.get_jt_cols(), '奖金模板-集团机关', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_gf_model = BaseExcelImportModel(
            SalaryBonus.NAME_GF, SalaryBonus, SalaryBonus.get_gf_cols(), '奖金模板-股份', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_jp_model = BaseExcelImportModel(
            SalaryBonus.NAME_JP, SalaryBonus, SalaryBonus.get_jp_cols(), '奖金模板-教培', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_xw_model = BaseExcelImportModel(
            SalaryBonus.NAME_XW, SalaryBonus, SalaryBonus.get_xw_cols(), '奖金模板-新闻', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_lt_model = BaseExcelImportModel(
            SalaryBonus.NAME_LT, SalaryBonus, SalaryBonus.get_lt_cols(), '奖金模板-离退休', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_bw_model = BaseExcelImportModel(
            SalaryBonus.NAME_BWB, SalaryBonus, SalaryBonus.get_bwb_cols(), '奖金模板-保卫部', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        util = XlsToModelUtil(
            [s_p_model, s_j_model, s_b_model, s_gz_model, s_jj_model, s_a_model, s_bo_jt_model, s_bo_gf_model, s_bo_jp_model, s_bo_xw_model, s_bo_lt_model, s_bo_bw_model])
        res: dict = util.load_tpls()
        assert SalaryPerson.name_key in res
        assert len(res[SalaryPerson.name_key]) > 0
        assert len(res[SalaryPerson.name_key][0]["马鞍山钢铁股份有限公司（总部）"]) > 0
        assert res[SalaryPerson.name_key][0]["马鞍山钢铁股份有限公司（总部）"]["34_港务原料总厂1"]["M74244"]._name == "万利军"
        assert res[SalaryPerson.name_key][1]["马鞍山钢铁股份有限公司（总部）"]["34_港务原料总厂1"]["511022198105215653"]._name == "万利军"
        assert res[SalaryPerson.name_key][1]["马鞍山钢铁股份有限公司（总部）"]["34_港务原料总厂1"]["511022198105215653"].period.period == "202102"
        assert SalaryJob.name_key in res
        assert len(res[SalaryJob.name_key]) > 0
        assert res[SalaryJob.name_key]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._code == 'M04484'
        assert res[SalaryJob.name_key]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._name == '汤寅波'
        assert res[SalaryJob.name_key]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._zx_jobname == '经理'
        assert SalaryBank.name_key in res
        assert len(res[SalaryBank.name_key]) > 0
        assert res[SalaryBank.name_key]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]['gz']._code == 'M04484'
        assert res[SalaryBank.name_key]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]['jj']._code == 'M04484'

        assert SalaryGz.name_key in res
        assert len(res[SalaryGz.name_key]) > 0
        assert res[SalaryGz.name_key]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._code == 'M73677'
        assert SalaryJj.name_key in res
        assert len(res[SalaryJj.name_key]) > 0
        assert res[SalaryJj.name_key]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._code == 'M73677'
        assert res[SalaryJj.name_key]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M80374"]._totalPayable == 4965 * 3

        assert SalaryAttendance.name_key in res
        assert len(res[SalaryAttendance.name_key]) > 0

        assert SalaryBonus.NAME_JT in res
        assert len(res[SalaryBonus.NAME_JT]) > 0
        assert res[SalaryBonus.NAME_JT]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._name == "童坦"

        assert SalaryBonus.NAME_GF in res
        assert len(res[SalaryBonus.NAME_GF]) > 0
        assert "02_股份机关" in res[SalaryBonus.NAME_GF]["马鞍山钢铁股份有限公司（总部）"]

        assert SalaryBonus.NAME_JP in res
        assert len(res[SalaryBonus.NAME_JP]) > 0
        assert "M73677" not in res[SalaryBonus.NAME_JP]["马钢（集团）控股有限公司(总部)"]["C5_教培中心"]
        assert res[SalaryBonus.NAME_JP]["马钢（集团）控股有限公司(总部)"]["C5_教培中心"]["M19391"]._code == "M19391"

        assert SalaryBonus.NAME_XW in res
        assert len(res[SalaryBonus.NAME_XW]) > 0
        assert "M73677" not in res[SalaryBonus.NAME_XW]["马钢（集团）控股有限公司(总部)"]["C2_新闻中心"]
        assert res[SalaryBonus.NAME_XW]["马钢（集团）控股有限公司(总部)"]["C2_新闻中心"]["M02830"]._code == "M02830"

        assert SalaryBonus.NAME_LT in res
        assert len(res[SalaryBonus.NAME_LT]) > 0
        assert "M73677" not in res[SalaryBonus.NAME_LT]["马钢（集团）控股有限公司(总部)"]["C3_离退休职工服务中心"]
        assert res[SalaryBonus.NAME_LT]["马钢（集团）控股有限公司(总部)"]["C3_离退休职工服务中心"]["M32812"]._code == "M32812"

        assert SalaryBonus.NAME_BWB in res
        assert len(res[SalaryBonus.NAME_BWB]) > 0
        assert "M32812" not in res[SalaryBonus.NAME_BWB]["马钢（集团）控股有限公司(总部)"]["C1_保卫部（武装部）"]
        assert res[SalaryBonus.NAME_BWB]["马钢（集团）控股有限公司(总部)"]["C1_保卫部（武装部）"]["M72717"]._code == "M72717"

    def test_load_tex_tpls(self):

        cols = cols = SalaryPeriod.cols()
        sp_model = BaseExcelImportModel(
            "sp", SalaryPeriod, cols, '当前审核日期', None, convertor=SalaryPeriodConventor())
        util = XlsToModelUtil([sp_model])
        res: dict = util.load_tpls()
        assert "sp" in res
        assert res["sp"].year == 2021
        assert res["sp"].month == 2
        period = res["sp"]

        sd_model = BaseExcelImportModel(
            SalaryDepart.name_key, SalaryDepart, SalaryDepart.cols(), '审核机构信息', None, convertor=SalaryDepartConventor(), period=period)

        util = XlsToModelUtil([sd_model])
        res: dict = util.load_tpls()
        assert '202102' == sd_model.period.period
        assert SalaryDepart.name_key in res
        assert len(res[SalaryDepart.name_key]) > 0
        assert "01" in res[SalaryDepart.name_key]
        departs = res[SalaryDepart.name_key]

        s_p_model = BaseExcelImportModel(
            SalaryPerson.name_key, SalaryPerson, SalaryPerson.cols(), '', '人员信息', convertor=SalaryPersonConventor(), period=period, departs=departs)
        s_gz_model = BaseExcelImportModel(
            SalaryGz.name_key, SalaryGz, SalaryGz.cols(), '', '工资信息', convertor=SalaryGzConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        s_jj_model = BaseExcelImportModel(
            SalaryJj.name_key, SalaryJj, SalaryJj.cols(), '', '奖金信息', convertor=SalaryJjConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        util = XlsToModelUtil([s_p_model, s_gz_model, s_jj_model])
        res: dict = util.load_tpls()
        persons = res[SalaryPerson.name_key]
        tex_util = TexXlsToModelUtil(
            period, departs, persons, res[SalaryGz.name_key], res[SalaryJj.name_key])
        tex_res: dict = tex_util.load_tex_tpls()
        assert len(tex_res) > 0
        assert "M32812" not in tex_res["马钢（集团）控股有限公司(总部)"]["C1_保卫部（武装部）"]
