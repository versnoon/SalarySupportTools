#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine_two.py
@Time    :   2021/01/26 16:33:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import isfile, exists
from os import makedirs, listdir, remove
from shutil import rmtree

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

    def split_salary_data_by_depart(self, departs, gz_datas, jj_datas):
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
            if self._need_audit_by_depart(departs, k):
                gz_map[k] = gz_values
        jj_map = OrderedDict()

        for jj in jj_datas:
            jj_values = []
            k = jj.depart
            if k in jj_map:
                jj_values = jj_map[k]
            jj_values.append(jj)
            if self._need_audit_by_depart(departs, k):
                jj_map[k] = jj_values
        return gz_map, jj_map

    def _need_audit_by_depart(self, departs, departname):
        """
        当为空的时候不进行操作
        """
        for k, v in departs.items():
            if departname == v.get_depart_salaryScope_and_name():
                return v.status is not None and v.status != ''
        return False

    def copy_to_depart_folder(self, period, gz_datas, jj_datas, errs_mgs):
        """
        写入相应的单位文件夹
        """
        # 清理已有文件
        gz = SalaryGzInfo()
        gz_columndef = gz.getColumnDef()
        for k, v in gz_datas.items():
            if k not in errs_mgs:
                self.createExcel(period, k, "工资信息", v, gz_columndef)
        jj = SalaryJjInfo()
        jj_columndef = jj.getColumnDef()
        for k, v in jj_datas.items():
            if k not in errs_mgs:
                self.createExcel(period, k, "奖金信息", v, jj_columndef)

    def clear_excel(self, period, departs):
        for depart in departs.values():
            self._clearExcel(
                period, depart.get_depart_salaryScope_and_name(), "工资信息.xls")
            self._clearExcel(
                period, depart.get_depart_salaryScope_and_name(), "奖金信息.xls")
            path = r'{}\{}\{}\{}'.format(
                self._folder_prefix, period, depart.get_depart_salaryScope_and_name(), "导出文件")
            if exists(path):
                rmtree(path)

    def _clearExcel(self, period, depart_folder_name, filename):
        path = r'{}\{}\{}\{}'.format(
            self._folder_prefix, period, depart_folder_name, filename)
        if exists(path):
            remove(path)

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

    def validate(self, period, persons, banks, depart, gzm, jjm):
        """
        验证工资数据，验证奖金数据
        """
        # 验证工资
        #  实发 < 0
        #  缺少工资账号
        #  岗位绩效  缺少岗位工资
        #  生活费   岗位工资不为0
        err_mgs = dict()
        for depart, vs in gzm.items():
            err_message = []
            for v in vs:
                if depart in err_mgs:
                    err_message = err_mgs[depart]
                if v._pay < 0:
                    err_message.append(self.err_mss(
                        persons[v._code], "工资实发异常：工资实发小于0，实发金额{}".format(v._pay)))
                bankno = banks[v._code]["gz"]
                if v._pay > 0 and (bankno._bankNo is None or bankno._bankNo == "" or bankno._departfullinfo != v._departfullinfo):
                    err_message.append(self.err_mss(
                        persons[v._code], "银行卡信息异常：缺少工资卡信息"))
                if v._salaryModel.startswith("岗位绩效工资制") and v._gwgz == 0:
                    err_message.append(self.err_mss(
                        persons[v._code], "岗位工资异常：缺少岗位工资信息"))
                if v._salaryModel.startswith("生活费") and v._shf == v._totalPayable:
                    err_message.append(self.err_mss(
                        persons[v._code], "生活费人员工资异常：其他工资{}不等于应发合计{}".format(v._shf, v._totalPayable)))
            if len(err_message) > 0:
                err_mgs[depart] = err_message
        # 验证奖金
        # 实发  < 0
        # 缺少哦奖金账号
        for depart, vs in jjm.items():
            err_message = []
            for v in vs:
                if depart in err_mgs:
                    err_message = err_mgs[depart]
                if v._pay < 0:
                    err_message.append(self.err_mss(
                        persons[v._code], "奖金实发异常：奖金实发小于0，实发金额{}".format(v._pay)))
                bankno = banks[v._code]["jj"]
                if v._pay > 0 and (bankno._bankNo is None or bankno._bankNo == "" or bankno._departfullinfo != v._departfullinfo):
                    err_message.append(self.err_mss(
                        persons[v._code], "银行卡信息异常：缺少奖金卡信息"))
            if len(err_message) > 0:
                err_mgs[depart] = err_message
        return err_mgs

    def err_mss(self, person, message) -> str:
        return '错误信息提示:  ->  {}--{}'.format(person, message)

    def err_info_write_to_depart_folder(self, period, errs_mgs):
        """
        写入相应得文件夹
        """
        for i, v in errs_mgs.items():
            path = r'{}\{}\{}\{}'.format(
                self._folder_prefix, period, i, "错误信息.txt")
            if exists(path):
                remove(path)
            if len(v) > 0:
                with open(path, 'a', encoding='utf-8') as f:
                    for i in range(len(v)):
                        msg = v[i]
                        f.write('{} {}'.format(i+1, msg + '\n'))
        return errs_mgs
