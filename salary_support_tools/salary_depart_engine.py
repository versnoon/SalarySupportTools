#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_depart_engine.py
@Time    :   2021/01/28 16:04:00
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com

'''

from os.path import exists
from os import makedirs
from collections import OrderedDict

from salary_support_tools.exl_to_clazz import ExlToClazz


class SalaryDepartEngine(object):

    def __init__(self, period):
        self.name = "salary_depart"
        self._period = period
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        return self.load_data()

    def load_data(self):
        sd = SalaryDepart()
        sd_load = ExlToClazz(SalaryDepart, sd.getColumnDef(),
                             self.get_exl_tpl_folder_path())
        sds = sd_load.loadTemp()
        # 初始化日期文件夹 工作目录
        if len(sds) < 1:
            raise ValueError("审核机构解析错误,请检查'审核机构信息.xls'模板")
        sdm = sd.to_map(sds)
        return sdm

    def get_exl_tpl_folder_path(self):
        return r'{}\{}'.format(self._folder_prefix, "审核机构信息.xls")


class SalaryDepart(object):
    def __init__(self):
        self.salaryScope = ""  # 工资范围
        self.name = ""  # 单位名称
        self.sortno = 0  # 显示顺序
        self.relativeUnits = ""  # 相关单位
        self.status = ""  # 审核状态 不为空 及做数据的输出和导出 空不做动作
        self.texdepart = ""  # "税务机构"

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["sortno"] = "序号"
        columns["salaryScope"] = "工资范围"
        columns["name"] = "EHR单位名称"
        columns["relativeUnits"] = "相关单位"
        columns["status"] = "审核状态"
        columns["texdepart"] = "税务机构"
        return columns

    def to_map(self, datas):
        m = OrderedDict()
        if datas is not None and len(datas) > 0:
            for i in datas:
                k = i.salaryScope
                m[k] = i
        return m

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

    def __str__(self):
        return '审核机构信息: 序号{} - 工资范围 {} - 审核单位名称 {} - 相关单位 {}'.format(self.sortno, self.salaryScope, self.name, self.get_departs())
