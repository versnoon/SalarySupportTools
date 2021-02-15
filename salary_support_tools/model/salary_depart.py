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


class SalaryDepart:
    """
    审核单位相关信息
    """

    def __init__(self):
        self.salaryScope = ""  # 工资范围
        self.name = ""  # 单位名称
        self.sortno = 0  # 显示顺序
        self.relativeUnits = ""  # 相关单位
        self.status = ""  # 审核状态 不为空 及做数据的输出和导出 空不做动作
        self.texdepart = ""  # "税务机构"

    def get_departs(self):
        res = []
        if self.relativeUnits is None or self.relativeUnits == "":
            res.append(self.name)
        else:
            res.extend(self.relativeUnits.split("|"))
        return res

    def get_depart_salaryScope_and_name(self):
        return '{}_{}'.format(self.salaryScope, self.name)

    def contain_relativeunits(self):
        """
        判断是否有相关单位
        """
        return len(self.relativeUnits) > 0

    def is_depart(self, departname):
        if self.name == departname:
            return True
        relativeUnits = self.get_departs()
        for unit in relativeUnits:
            if unit == departname:
                return True
        return False

    def need_audit(self):
        return self.status is None or self.status == ''

    @classmethod
    def cols(self):
        cols = dict()
        cols["sortno"] = "序号"
        cols["salaryScope"] = "工资范围"
        cols["name"] = "EHR单位名称"
        cols["relativeUnits"] = "相关单位"
        cols["status"] = "审核状态"
        cols["texdepart"] = "税务机构"
        return cols

    @classmethod
    def cov(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in datas:
                k = i.salaryScope
                m[k] = i
        return m

    def __str__(self):
        return '审核机构信息: 序号{} - 工资范围 {} - 审核单位名称 {} - 相关单位 {}'.format(self.sortno, self.salaryScope, self.name, self.get_departs())
