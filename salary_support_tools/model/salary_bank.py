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


class SalaryBank(BasePeriodEngine):
    """
    员工银行相关信息
    """

    NAME = "salary_bank"

    def __init__(self):
        super().__init__(None)
        self._code = ""
        self._name = ""
        self._departfullinfo = ""
        self._financialInstitution = ""
        self._bankNo = ""
        self._payment = ""
        self._purpose = ""
        self._associalBankNo = ""
        self._cardType = ""

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "部门"
        cols["_financialInstitution"] = "金融机构"
        cols["_bankNo"] = "卡号"
        cols["_payment"] = "支付方式"
        cols["_purpose"] = "卡用途"
        cols["_associalBankNo"] = "联行号/网点代码"
        cols["_cardType"] = "卡折类型"
        return cols


class SalaryBankConventor(BaseModelConventor):

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
            v = OrderedDict()
            if code in vs_depart:
                v = vs_depart[code]
            if self.is_gz_bankno(data._purpose):
                v['gz'] = data
            if self.is_jj_bankno(data._purpose):
                v['jj'] = data
            vs_depart[code] = v
            vs[depart_str] = vs_depart
            res[company] = vs

        return res

    def is_gz_bankno(self, purpose=""):
        return self.val_bank_purpost(purpose, "工资卡")

    def is_jj_bankno(self, purpose=""):
        return self.val_bank_purpost(purpose, "奖金卡")

    def val_bank_purpost(self, purpose="", banktype=""):
        if len(purpose) == 0:
            return False
        if len(banktype) == 0:
            return False
        if banktype in purpose:
            return True
        else:
            return False
