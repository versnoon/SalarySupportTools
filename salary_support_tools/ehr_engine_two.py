#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine_two.py
@Time    :   2021/01/26 16:33:34
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import isfile, exists, join
from os import makedirs, listdir

from collections import OrderedDict

import xlwt

from salary_support_tools.ehr_engine import SalaryPeriod
from salary_support_tools.ehr_engine import SalaryDepart
from salary_support_tools.ehr_engine import ExlsToClazz
from salary_support_tools.ehr_engine import ExlToClazz
from salary_support_tools.ehr_engine import PersonInfo
from salary_support_tools.ehr_engine import SalaryBankInfo
from salary_support_tools.ehr_engine import SalaryGzInfo
from salary_support_tools.ehr_engine import SalaryJjInfo


class EhrEngineTwo(object):
    """
    统一数据文件夹存放工资信息，奖金信息
    自动完成分文件夹及导出
    根据审核机构信息的标记进行审核
    """

    def __init__(self):
        self._name = "ehrEngineTwo"
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def initven(self):
        # 解析审核日期
        salaryPeriod = SalaryPeriod()
        sp = ExlToClazz(SalaryPeriod, salaryPeriod.getColumnDef(),
                        salaryPeriod.get_exl_tpl_folder_path())
        sps = sp.loadTemp()
        if len(sps) != 1:
            raise ValueError("审核日期解析错误,请检查'当前审核日期.xls'模板")
        period = salaryPeriod.get_period_str(sps[0].year, sps[0].month)

        # 初始化日期文件夹 单位目录
        current_folder_path = r"{}\{}".format(self._folder_prefix, period)
        if not exists(current_folder_path):
            makedirs(current_folder_path)
        # 解析单位信息模板

        salaryDepart = SalaryDepart()
        sd = ExlToClazz(SalaryDepart, salaryDepart.getColumnDef(),
                        salaryDepart.get_exl_tpl_folder_path())
        sds = sd.loadTemp()
        if len(sds) < 1:
            raise ValueError("审核机构解析错误,请检查'审核机构信息.xls'模板")
        dm = salaryDepart.to_map(sds)
        for k, v in dm.items():
            current_folder_path = r"{}\{}\{}".format(
                self._folder_prefix, period, v.get_depart_salaryScope_and_name())
            if not exists(current_folder_path):
                makedirs(current_folder_path)
        # 初始化工资数据，奖金数据存放目录

        current_folder_path = r"{}\{}\{}".format(
            self._folder_prefix, period, "工资奖金数据")
        if not exists(current_folder_path):
            makedirs(current_folder_path)

        return period, dm

    def loadBaseDatas(self, period):
        # 解析人员基本信息
        personInfo = PersonInfo()
        personInfo.period = period
        cov = ExlToClazz(
            PersonInfo, personInfo.getColumnDef(), personInfo.get_exl_tpl_folder_path())
        persons = personInfo.to_map(cov.loadTemp())
        # 解析银行卡信息数据
        salaryBankInfo = SalaryBankInfo()
        salaryBankInfo.period = period
        cov = ExlsToClazz(
            SalaryBankInfo, salaryBankInfo.getColumnDef(), salaryBankInfo.get_exl_tpl_folder_path_prefix(), salaryBankInfo.get_exl_tpl_file_name_prefix(), 0, True)
        salaryBanks = cov.loadTemp()
        banks = salaryBankInfo.to_map(salaryBanks)
        return persons, banks

    def loadAuditedDatas(self, period, departs):

        # 加载工资结果，奖金结果数据

        current_audited_folder_path = r"{}\{}\{}".format(
            self._folder_prefix, period, "工资奖金数据")
        # load gz
        # load jj

        gz = SalaryGzInfo()
        gz_cov = ExlsToClazz(
            SalaryGzInfo, gz.getColumnDef(), current_audited_folder_path, "工资信息")
        gz_datas = gz_cov.loadTemp()

        jj = SalaryJjInfo()
        jj_cov = ExlsToClazz(
            SalaryJjInfo, jj.getColumnDef(), current_audited_folder_path, "奖金信息")
        jj_datas = jj_cov.loadTemp()

        return self.set_period_and_depart(period, departs, gz_datas, jj_datas)

    def set_period_and_depart(self, period, departs, gzs, jjs):
        """
        设置工资奖金信息的期间信息和单位信息
        """
        for gz in gzs:
            gz.period = period
            di = gz._get_depart_from_departLevelTow(departs)
            if di is not None:
                gz.depart = di.get_depart_salaryScope_and_name()

        for jj in jjs:
            jj.period = period
            di = jj._get_depart_from_departfullinfo(departs)
            if di is not None:
                jj.depart = di.get_depart_salaryScope_and_name()
        return gzs, jjs

    def split_salary_data_by_depart(self, gz_datas, jj_datas):
        """
        将载入的工资数据和奖金数据根据单位信息分类
        """
        gz_map = OrderedDict()

        # 按照文件夹名称分类
        for gz in gz_datas:
            gz_values = []
            k = gz.depart
            if k in gz_map:
                gz_values = gz_map[k]
            gz_values.append(gz)
            gz_map[k] = gz_values
        jj_map = OrderedDict()

        for jj in jj_datas:
            jj_values = []
            k = jj.depart
            if k in jj_map:
                jj_values = jj_map[k]
            jj_values.append(jj)
            jj_map[k] = jj_values
        return gz_map, jj_map

    def copy_to_depart_folder(self, period, gz_datas, jj_datas):
        """
        写入相应的单位文件夹
        """
        gz = SalaryGzInfo()
        gz_columndef = gz.getColumnDef()
        for k, v in gz_datas.items():
            self.createExcel(period, k, "工资信息", v, gz_columndef)
        jj = SalaryJjInfo()
        jj_columndef = jj.getColumnDef()
        for k, v in jj_datas.items():
            self.createExcel(period, k, "奖金信息", v, jj_columndef)

    def createExcel(self, period, depart_folder_name, file_name, datas, columndefs):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet1')

        # 写入标题
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                try:
                    s.write(
                        i+1, j, getattr(datas[i], propertyName, 0))
                except TypeError:
                    print(propertyName)

        path = r'd:\薪酬审核文件夹\{}\{}'.format(period, depart_folder_name)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}{}'.format(path, file_name, ".xls"))
