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
        assert i_model.base_tpl_folder_path() == r'd:\薪酬审核文件夹'
        assert i_model.test_tpl_folder_path() == r'd:\薪酬审核文件夹\test'
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
            "s_p", SalaryPerson, SalaryPerson.cols(), '', '人员信息', convertor=SalaryPersonConventor(), period=period, departs=departs)
        s_j_model = BaseExcelImportModel(
            "s_j", SalaryJob, SalaryJob.cols(), '', '岗位聘用信息', convertor=SalaryJobConventor(), period=period, departs=departs)
        s_b_model = BaseExcelImportModel(
            "s_b", SalaryBank, SalaryBank.cols(), '', '银行卡信息', convertor=SalaryBankConventor(), period=period, departs=departs)
        s_gz_model = BaseExcelImportModel(
            "s_gz", SalaryGz, SalaryGz.cols(), '', '工资信息', convertor=SalaryGzConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        s_jj_model = BaseExcelImportModel(
            "s_jj", SalaryJj, SalaryJj.cols(), '', '奖金信息', convertor=SalaryJjConventor(), period=period, departs=departs, filefoldername='工资奖金数据')
        s_a_model = BaseExcelImportModel(
            "s_a", SalaryAttendance, SalaryAttendance.cols(), '', '考勤模板', convertor=SalaryAttendanceConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_jt_model = BaseExcelImportModel(
            "s_bo_jt", SalaryBonus, SalaryBonus.get_jt_cols(), '奖金模板-集团机关', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_gf_model = BaseExcelImportModel(
            "s_bo_gf", SalaryBonus, SalaryBonus.get_gf_cols(), '奖金模板-股份', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_jp_model = BaseExcelImportModel(
            "s_bo_jp", SalaryBonus, SalaryBonus.get_jp_cols(), '奖金模板-教培', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_xw_model = BaseExcelImportModel(
            "s_bo_xw", SalaryBonus, SalaryBonus.get_xw_cols(), '奖金模板-新闻', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_lt_model = BaseExcelImportModel(
            "s_bo_lt", SalaryBonus, SalaryBonus.get_lt_cols(), '奖金模板-离退休', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        s_bo_bw_model = BaseExcelImportModel(
            "s_bo_bwb", SalaryBonus, SalaryBonus.get_bwb_cols(), '奖金模板-保卫部', '', convertor=SalaryBonusConventor(), period=period, departs=departs, filefoldername='考勤奖金模板')
        util = XlsToModelUtil(
            [s_p_model, s_j_model, s_b_model, s_gz_model, s_jj_model, s_a_model, s_bo_jt_model, s_bo_gf_model, s_bo_jp_model, s_bo_xw_model, s_bo_lt_model, s_bo_bw_model])
        res: dict = util.load_tpls()
        assert "s_p" in res
        assert len(res["s_p"]) > 0
        assert len(res["s_p"][0]["马鞍山钢铁股份有限公司（总部）"]) > 0
        assert res["s_p"][0]["马鞍山钢铁股份有限公司（总部）"]["M74244"]._name == "万利军"
        assert res["s_p"][1]["马鞍山钢铁股份有限公司（总部）"]["511022198105215653"]._name == "万利军"
        assert res["s_p"][1]["马鞍山钢铁股份有限公司（总部）"]["511022198105215653"].period.period == "202102"
        assert "s_j" in res
        assert len(res["s_j"]) > 0
        assert res["s_j"]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._code == 'M04484'
        assert res["s_j"]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._name == '汤寅波'
        assert res["s_j"]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]._zx_jobname == '经理'
        assert "s_b" in res
        assert len(res["s_b"]) > 0
        assert res["s_b"]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]['gz']._code == 'M04484'
        assert res["s_b"]["马鞍山钢铁股份有限公司（总部）"]["02_股份机关"]["M04484"]['jj']._code == 'M04484'

        assert "s_gz" in res
        assert len(res["s_gz"]) > 0
        assert res["s_gz"]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._code == 'M73677'
        assert "s_jj" in res
        assert len(res["s_jj"]) > 0
        assert res["s_jj"]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._code == 'M73677'
        assert res["s_jj"]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M80374"]._totalPayable == 4965 * 3

        assert "s_a" in res
        assert len(res["s_a"]) > 0

        assert "s_bo_jt" in res
        assert len(res["s_bo_jt"]) > 0
        assert res["s_bo_jt"]["马钢（集团）控股有限公司(总部)"]["01_集团机关"]["M73677"]._name == "童坦"

        assert "s_bo_gf" in res
        assert len(res["s_bo_gf"]) > 0
        assert "02_股份机关" in res["s_bo_gf"]["马鞍山钢铁股份有限公司（总部）"]

        assert "s_bo_jp" in res
        assert len(res["s_bo_jp"]) > 0
        assert "M73677" not in res["s_bo_jp"]["马钢（集团）控股有限公司(总部)"]["C5_教培中心"]
        assert res["s_bo_jp"]["马钢（集团）控股有限公司(总部)"]["C5_教培中心"]["M19391"]._code == "M19391"

        assert "s_bo_xw" in res
        assert len(res["s_bo_xw"]) > 0
        assert "M73677" not in res["s_bo_xw"]["马钢（集团）控股有限公司(总部)"]["C2_新闻中心"]
        assert res["s_bo_xw"]["马钢（集团）控股有限公司(总部)"]["C2_新闻中心"]["M02830"]._code == "M02830"

        assert "s_bo_lt" in res
        assert len(res["s_bo_lt"]) > 0
        assert "M73677" not in res["s_bo_lt"]["马钢（集团）控股有限公司(总部)"]["C3_离退休职工服务中心"]
        assert res["s_bo_lt"]["马钢（集团）控股有限公司(总部)"]["C3_离退休职工服务中心"]["M32812"]._code == "M32812"

        assert "s_bo_bwb" in res
        assert len(res["s_bo_bwb"]) > 0
        assert "M32812" not in res["s_bo_bwb"]["马钢（集团）控股有限公司(总部)"]["C1_保卫部（武装部）"]
        assert res["s_bo_bwb"]["马钢（集团）控股有限公司(总部)"]["C1_保卫部（武装部）"]["M72717"]._code == "M72717"

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
            "sd", SalaryDepart, SalaryDepart.cols(), '审核机构信息', None, convertor=SalaryDepartConventor(), period=period)

        util = XlsToModelUtil([sd_model])
        res: dict = util.load_tpls()
        assert '202102' == sd_model.period.period
        assert "sd" in res
        assert len(res["sd"]) > 0
        assert "01" in res["sd"]
        departs = res["sd"]
        tex_util = TexXlsToModelUtil(period, departs)
        tex_res: dict = tex_util.load_tex_tpls()
        assert len(tex_res) > 0
