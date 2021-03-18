#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SalaryPeriod.py
@Time    :   2021/02/13 11:48:32
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SalaryJj(BasePeriodEngine):
    """
    员工奖金相关信息
    """

    NAME = "salary_jj"

    def __init__(self):
        super().__init__(None)
        self.depart = ""  # 审批单位文件夹名称
        self.tex_depart = ""  # 税务机构
        self._code = ""
        self._name = ""
        self._depart_fullname = ""
        self._distributionMark = ""
        self._ysjse = 0
        self._bonusTwo = 0
        self._gtsyj = 0
        self._pay = 0
        self._jjhj = 0
        self._jsjseptsl = 0
        self._jbjj = 0
        self._gts = 0
        self._bonusOne = 0
        self._bonusThree = 0
        self._yseyhsl = 0
        self._yse = 0
        self._totalPayable = 0
        self._gstz = 0
        self._gcjj = 0
        self._jssc = 0
        self._nddxj = 0
        self._jsjj = 0
        self._qt = 0
        self._gsxyj = 0
        self._zxj = 0   # 重点工作专项奖
        self._ryj = 0   # 荣誉类奖

    def __str__(self):
        return '员工奖金信息: 机构 {} - 工号 {} - 姓名 {} - 应发 {} - 实发 {}'.format(self._depart_fullname, self._code, self._name, self._totalPayable, self._pay)

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "机构"
        cols["_distributionMark"] = "是否代发工资"
        cols["_ysjse"] = "应税计算额(优惠税率)"
        cols["_bonusTwo"] = "单项奖2"
        cols["_gtsyj"] = "个调税(应缴)"
        cols["_pay"] = "实发"
        cols["_jjhj"] = "奖金合计"
        cols["_jsjseptsl"] = "应税计算额(普通税率)"
        cols["_jbjj"] = "基本奖金"
        cols["_gts"] = "个调税"
        cols["_bonusOne"] = "单项奖1"
        cols["_bonusThree"] = "单项奖3"
        cols["_yseyhsl"] = "应税额(优惠税率)"
        cols["_bonusThree"] = "单项奖3"
        cols["_yseyhsl"] = "应税额"
        cols["_totalPayable"] = "应发"
        cols["_gstz"] = "个税调整"
        cols["_gcjj"] = "工程津贴"
        cols["_jssc"] = "技术输出"
        cols["_qt"] = "争取国家政策奖"
        cols["_nddxj"] = "年底兑现奖"
        cols["_jsjj"] = "计税奖金"
        cols["_zxj"] = "重点工作专项奖"
        cols["_ryj"] = "荣誉类奖"
        return cols


class SalaryJjConventor(BaseModelConventor):

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
            if code in vs_depart:
                data = self.to_sum(data, vs_depart[code])
            vs_depart[code] = data
            vs[depart_str] = vs_depart
            res[company] = vs
        return res

    def to_sum(self, jj1, jj2: SalaryJj):
        res = SalaryJj()
        res.period = jj1.period
        res.depart = jj1.depart  # 审批单位文件夹名称
        res.tex_depart = jj1.tex_depart  # 税务机构
        res._code = jj1._code
        res._name = jj1._name
        res._depart_fullname = jj1._depart_fullname
        res._distributionMark = jj1._distributionMark
        res._ysjse = jj1._ysjse + jj2._ysjse
        res._bonusTwo = jj1._bonusTwo + jj2._bonusTwo
        res._gtsyj = jj1._gtsyj + jj2._gtsyj
        res._pay = jj1._pay + jj2._pay
        res._jjhj = jj1._jjhj + jj2._jjhj
        res._jsjseptsl = jj1._jsjseptsl + jj2._jsjseptsl
        res._jbjj = jj1._jbjj + jj2._jbjj
        res._gts = jj1._gts + jj2._gts
        res._bonusOne = jj1._bonusOne + jj2._bonusOne
        res._bonusThree = jj1._bonusThree + jj2._bonusThree
        res._yseyhsl = jj1._yseyhsl + jj2._yseyhsl
        res._yse = jj1._yse + jj2._yse
        res._totalPayable = jj1._totalPayable + jj2._totalPayable
        res._gstz = jj1._gstz + jj2._gstz
        res._gcjj = jj1._gcjj + jj2._gcjj
        res._jssc = jj1._jssc + jj2._jssc
        res._nddxj = jj1._nddxj + jj2._nddxj
        res._jsjj = jj1._jsjj + jj2._jsjj
        res._qt = jj1._qt + jj2._qt
        res._gsxyj = jj1._gsxyj + jj2._gsxyj
        return res
