#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_bank_engine.py
@Time    :   2021/01/28 16:27:04
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from collections import defaultdict

from salary_support_tools.exl_to_clazz import ExlsToClazz


class SalaryBankEngine(object):

    def __init__(self, period, departs):
        self._name = "salary_bank"
        self._period = period
        self._departs = departs
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        return self.load_data()

    def load_data(self):
        salaryBankInfo = SalaryBankInfo()
        cov = ExlsToClazz(
            SalaryBankInfo, salaryBankInfo.getColumnDef(), self.get_exl_tpl_folder_path_prefix(), self.get_exl_tpl_file_name_prefix(), 0, True)
        salaryBanks = cov.loadTemp()
        return salaryBankInfo.to_map(salaryBanks, self._departs)

    def get_exl_tpl_folder_path_prefix(self):
        return r'{}\{}'.format(self._folder_prefix, self._period)

    def get_exl_tpl_file_name_prefix(self):
        return '银行卡信息'


class SalaryBankInfo(object):
    """
    银行卡信息
    """

    def __init__(self):
        self._code = ""
        self._name = ""
        self._departfullinfo = ""
        self._financialInstitution = ""
        self._bankNo = ""
        self._payment = ""
        self._purpose = ""
        self._associalBankNo = ""
        self._cardType = ""

    def __str__(self):
        return '员工银行卡信息: 机构 {} - 工号 {} - 姓名 {} - 金融机构 {} - 卡号 {}'.format(self._departfullinfo, self._code, self._name, self._financialInstitution, self._bankNo)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "部门"
        columns["_financialInstitution"] = "金融机构"
        columns["_bankNo"] = "卡号"
        columns["_payment"] = "支付方式"
        columns["_purpose"] = "卡用途"
        columns["_associalBankNo"] = "联行号/网点代码"
        columns["_cardType"] = "卡折类型"

        return columns

    def to_map(self, datas, departs):

        # 按单位分组
        ds = defaultdict(lambda: None)
       # for k, depart in departs.items():
       # depart_str = depart.get_depart_salaryScope_and_name()
        if datas is not None and len(datas) > 0:
            m = defaultdict(lambda: None)
            for i in range(len(datas)):
                info = datas[i]
                bank_depart = info._get_depart_from_departfullinfo(departs)
                for k, depart in departs.items():
                    depart_str = depart.get_depart_salaryScope_and_name()
                    # 分组
                    if bank_depart is not None and depart.salaryScope == bank_depart.salaryScope:
                        if depart_str in ds:
                            m = ds[depart_str]
                        v = defaultdict(lambda: None)
                        if info._code in m:
                            v = m[info._code]
                        if self.is_gz_bankno(info._purpose):
                            v['gz'] = info
                        if self.is_jj_bankno(info._purpose):
                            v['jj'] = info
                        if len(v) > 0:
                            m[info._code] = v
                        if len(m) > 0:
                            ds[depart_str] = m
        return ds

    def _get_departLevelTow(self, i=1):
        departs = self._departfullinfo.split("\\")
        if len(departs) < 2:
            raise ValueError(
                "机构信息错误：{}-{}".format(self._code, self._departfullinfo))
        return departs[i]

    def _get_depart_from_departfullinfo(self, departs):
        for k, v in departs.items():
            relativeUnits = v.get_departs()
            for ru in relativeUnits:
                i = 1
                if k == '49':  # 投资工资 取 1
                    i = 0
                if self._get_departLevelTow(i) == ru:
                    return v
        return None

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
