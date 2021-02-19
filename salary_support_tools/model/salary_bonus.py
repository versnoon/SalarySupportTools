#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_attendance.py
@Time    :   2021/02/19 08:56:37
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from collections import OrderedDict

from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SalaryBonus(BasePeriodEngine):
    """
    奖金模板载入
    """

    NAME = "salary_bonus"
    NAME_JT = "salary_bonus_jt"
    NAME_GF = "salary_bonus_gf"
    NAME_JP = "salary_bonus_jp"
    NAME_XW = "salary_bonus_xw"
    NAME_LT = "salary_bonus_lt"
    NAME_BWB = "salary_bonus_BWB"

    def __init__(self):
        super().__init__(None)
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._depart_fullname = ""  # 所在机构
        self._depart_desc = 0  # 发放机构(默认为员工所在机构)
        self._nddx = 0  # 年底兑现奖
        self._dj1 = 0  # 单项奖1
        self._dj2 = 0  # 单项奖2
        self._dj3 = 0  # 单项奖3
        self._jbj = 0  # 基本奖金
        self._gstz = 0  # 个税调整
        self._jsj = 0  # 计税奖金

    @classmethod
    def get_gf_cols(self) -> dict:
        """
        股份本部
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652347)"
        cols["_dj1"] = "单项奖1(2652349)"
        cols["_dj2"] = "单项奖2(2652343)"
        cols["_dj3"] = "单项奖3(2652350)"
        cols["_jbj"] = "基本奖金(2652344)"
        cols["_gstz"] = "个税调整(2653810)"
        cols["_jsj"] = "计税奖金(2652342)"
        return cols

    @classmethod
    def get_jt_cols(self) -> dict:
        """
        集团机关
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652030)"
        cols["_dj1"] = "单项奖1(2652026)"
        cols["_dj2"] = "单项奖2(2652027)"
        cols["_dj3"] = "单项奖3(2652028)"
        cols["_jbj"] = "基本奖金(2652029)"
        cols["_gstz"] = "个税调整(2653745)"
        cols["_jsj"] = "计税奖金(2652031)"
        return cols

    @classmethod
    def get_jp_cols(self) -> dict:
        """
        教培
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652356)"
        cols["_dj1"] = "单项奖1(2652358)"
        cols["_dj2"] = "单项奖2(2652352)"
        cols["_dj3"] = "单项奖3(2652359)"
        cols["_jbj"] = "基本奖金(2652353)"
        cols["_gstz"] = "个税调整(2653811)"
        cols["_jsj"] = "计税奖金(2652351)"
        return cols

    @classmethod
    def get_xw_cols(self) -> dict:
        """
        新闻
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652374)"
        cols["_dj1"] = "单项奖1(2652376)"
        cols["_dj2"] = "单项奖2(2652370)"
        cols["_dj3"] = "单项奖3(2652377)"
        cols["_jbj"] = "基本奖金(2652371)"
        cols["_gstz"] = "个税调整(2653812)"
        cols["_jsj"] = "计税奖金(2652369)"
        return cols

    @classmethod
    def get_lt_cols(self) -> dict:
        """
        离退休
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652365)"
        cols["_dj1"] = "单项奖1(2652367)"
        cols["_dj2"] = "单项奖2(2652361)"
        cols["_dj3"] = "单项奖3(2652368)"
        cols["_jbj"] = "基本奖金(2652362)"
        cols["_gstz"] = "个税调整(2653813)"
        cols["_jsj"] = "计税奖金(2652360)"
        return cols

    @classmethod
    def get_bwb_cols(self) -> dict:
        """
        保卫部
        """
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "所在机构"
        cols["_depart_desc"] = "发放机构(默认为员工所在机构)"
        cols["_nddx"] = "年底兑现奖(2652392)"
        cols["_dj1"] = "单项奖1(2652394)"
        cols["_dj2"] = "单项奖2(2652388)"
        cols["_dj3"] = "单项奖3(2652395)"
        cols["_jbj"] = "基本奖金(2652389)"
        cols["_gstz"] = "个税调整(2653814)"
        cols["_jsj"] = "计税奖金(2652387)"
        return cols


class SalaryBonusConventor(BaseModelConventor):

    def cov(self, datas, period, departs):
        res = OrderedDict()
        for data in datas:
            data.period = period
            company, depart_str = self._get_depart_byfullname(
                data._depart_fullname, departs)
            code = data._code
            vs = OrderedDict()
            vs_depart = OrderedDict()
            if company in res:
                vs = res[company]
            if depart_str in vs:
                vs_depart = vs[depart_str]
            vs_depart[code] = data
            vs[depart_str] = vs_depart
            res[company] = vs
        return res

    def _get_depart_byfullname(self, depart_fullname, departinfos):
        departs = depart_fullname.split("\\")
        if len(departs) < 1:
            raise ValueError("{},机构信息异常".format(depart_fullname))
        depart_name = departs[0]
        company = ""
        for ds, depart in departinfos.items():
            if depart.is_depart(depart_name):
                depart_name = depart.get_depart_salaryScope_and_name()
                company = depart.texdepart
                break

        return company, depart_name
