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


class SalaryAttendance(BasePeriodEngine):
    """
    考勤模板载入
    """

    NAME = "salary_attend"

    def __init__(self):
        super().__init__(None)
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._depart_fullname = ""  # 员工部门
        self._dyb = 0  # 大夜班天数

        self._bj = 0  # 病假天数
        self._hj = 0  # 婚假天数
        self._shj = 0  # 事假天数
        self._sj = 0  # 丧假天数
        self._fdjb = 0  # 法定假日加班天数
        self._gxrjb = 0  # 公休日加班天数
        self._btj = 0  # 保胎假天数
        self._tqj = 0  # 探亲假
        self._xyb = 0  # 小夜班天数
        self._gs = 0  # 工伤假
        self._cj = 0  # 产假

        self._hlj = 0  # 护理假天数
        self._baoj = 0  # 保健天数
        self._zb = 0  # 值班个数
        self._dsb = 0  # 大三班天数

        self._kg = 0  # 旷工天数
        self._nxj = 0  # 年休假

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "员工部门"
        cols["_dyb"] = "大夜班天数"
        cols["_bj"] = "病假天数"
        cols["_hj"] = "婚假天数"
        cols["_shj"] = "事假天数"
        cols["_sj"] = "丧假天数"
        cols["_fdjb"] = "法定假日加班天数"
        cols["_gxrjb"] = "公休日加班天数"
        cols["_btj"] = "保胎假天数"
        cols["_tqj"] = "探亲假"
        cols["_xyb"] = "小夜班天数"
        cols["_gs"] = "工伤假"
        cols["_cj"] = "产假"
        cols["_hlj"] = "护理假天数"
        cols["_baoj"] = "保健天数"
        cols["_zb"] = "值班个数"
        cols["_dsb"] = "大三班天数"
        cols["_kg"] = "旷工天数"
        cols["_nxj"] = "年休假"
        return cols


class SalaryAttendanceConventor(BaseModelConventor):

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
