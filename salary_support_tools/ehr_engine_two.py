#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine_two.py
@Time    :   2021/01/26 16:33:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.exl_to_clazz import ExlToClazz
from salary_support_tools.exl_to_clazz import ExlsToClazz
from os.path import isfile, exists
from os import makedirs, listdir, remove
import time
from shutil import rmtree

from collections import OrderedDict

import xlwt

from salary_support_tools.person_engine import PersonEngine
from salary_support_tools.salary_period_engine import SalaryPeriodEngine
from salary_support_tools.salary_depart_engine import SalaryDepartEngine
from salary_support_tools.salary_bank_engine import SalaryBankEngine
from salary_support_tools.salary_gz_engine import SalaryGzEngine, SalaryGzInfo
from salary_support_tools.salary_jj_engine import SalaryJjEngine, SalaryJjInfo
from salary_support_tools.person_salary_engine import PersonSalaryInfo


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
        # 初始化审核环境
        # 1  读取日期模板，获取当前审核日期信息并完成目录建立
        # 2  读取单位信息模板，获取当前审核单位信息并完成目录建立
        # 3  建立工资奖金文件夹

        # 解析审核日期
        spe = SalaryPeriodEngine()
        period, _ = spe.start()
        # 解析单位信息模板

        sde = SalaryDepartEngine(period)
        dm = sde.start()
        # 初始化工资数据，奖金数据存放目录

        current_folder_path = r"{}\{}\{}".format(
            self._folder_prefix, period, "工资奖金数据")
        if not exists(current_folder_path):
            makedirs(current_folder_path)

        return period, dm

    def loadBaseDatas(self, period, departs):
        # 解析人员基本信息
        p_engine = PersonEngine(period)
        persons = p_engine.load_data()
        # 解析银行卡信息数据

        sb_engine = SalaryBankEngine(period, departs)
        banks = sb_engine.load_data()
        return persons, banks

    def loadAuditedDatas(self, period, departs):

        # 加载工资结果，奖金结果数据

        gz_engine = SalaryGzEngine(period)
        gz_datas = gz_engine.batch_load_data(departs)

        jj_engine = SalaryJjEngine(period)
        jj_datas = jj_engine.batch_load_data(departs)

        return gz_datas, jj_datas

    def write_audited_info(self, period, gz_datas, jj_datas, errs_mgs):
        """
        将审核结果写入txt文件
        """
        auditorinfo = AuditorInfo()
        aus = auditorinfo.create_auditorinfos(period, gz_datas, jj_datas)
        for k, vs in aus.items():
            if k not in errs_mgs:
                otherStyleStr = time.strftime(
                    "%Y%m%d%H%M%S", time.localtime(int(time.time())))
                path = r'{}\{}\{}\{}{}{}'.format(
                    self._folder_prefix, period, k, "审核结果", otherStyleStr, ".txt")
                with open(path, 'a', encoding='utf-8') as f:
                    f.write('{}'.format(vs))

    def clear_file(self, period, departs):
        """
        清楚上次得审核结果信息
        """
        for depart in departs.values():
            self._clearExcel(
                period, depart.get_depart_salaryScope_and_name(), "工资信息.xls")
            self._clearExcel(
                period, depart.get_depart_salaryScope_and_name(), "奖金信息.xls")
            self._clearExcel(
                period, depart.get_depart_salaryScope_and_name(), "错误信息.txt")
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

    def validate(self, period, persons, banks, departs, gzm, jjm):
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
                        persons, v._code, "工资实发异常：工资实发小于0，实发金额{}".format(v._pay)))
                bank = banks[depart][v._code]
                bankno = None
                if bank is not None:
                    bankno = banks[depart][v._code]["gz"]
                if v._pay > 0 and (bankno is None or bankno._bankNo is None or bankno._bankNo == ""):
                    err_message.append(self.err_mss(
                        persons, v._code, "银行卡信息异常：缺少工资卡信息"))
                if v._salaryModel.startswith("岗位绩效工资制") and v._gwgz == 0:
                    err_message.append(self.err_mss(
                        persons, v._code, "岗位工资异常：缺少岗位工资信息"))
                # if v._salaryModel.startswith("生活费") and v._shf != v._totalPayable:
                #     err_message.append(self.err_mss(
                #         persons, v._code, "生活费人员工资异常：其他工资{}不等于应发合计{}".format(v._shf, v._totalPayable)))
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
                        persons, v._code, "奖金实发异常：奖金实发小于0，实发金额{}".format(v._pay)))
                bank = banks[depart][v._code]
                bankno = None
                if bank is not None:
                    bankno = banks[depart][v._code]["jj"]
                if v._pay > 0 and (bankno is None or bankno._bankNo is None or bankno._bankNo == ""):
                    err_message.append(self.err_mss(
                        persons, v._code, "银行卡信息异常：缺少奖金卡信息"))
            if len(err_message) > 0:
                err_mgs[depart] = err_message
        return err_mgs

    def err_mss(self, persons, code, message) -> str:
        if code in persons:
            return '错误信息提示:  ->  {}--{}'.format(persons[code], message)
        else:
            return '错误信息提示:  ->  {}--{}'.format(code, message)

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


class AuditorInfo(object):
    """
    审核结果
    """

    def __init__(self):
        self.period = ""  # 薪酬期间
        self.depart = ""  # 单位信息
        self.numofpers = 0  # 发薪人数
        self.totalpayable = 0  # 应发合计
        self.pay = 0  # 实发合计
        self.tex = 0  # 所得税合计
        self.gjj_gr = 0  # 公积金个人
        self.yl_gr = 0  # 养老保险个人
        self.sy_gr = 0  # 失业保险个人
        self.yil_gr = 0  # 医疗保险个人
        self.nj_gr = 0  # 年金个人
        self.gjj_qy = 0  # 公积金企业
        self.yl_qy = 0  # 养老保险企业
        self.sy_qy = 0  # 失业保险企业
        self.yil_qy = 0  # 医疗保险企业
        self.nj_qy = 0  # 年金企业
        self.gs_qy = 0  # 工伤保险企业
        self.shy_qy = 0  # 生育企业

    def __str__(self):
        return '审核结果:  基本信息--> 发薪期间 {} - 发薪单位 {} - 发薪人数 {} | 薪酬信息 - -> 应发合计 {:.2f} - 实发合计 {:.2f} - 代缴信息 -->  所得税 {:.2f} - 公积金个人 {:.2f} - 公积金企业 {:.2f} - 养老个人 {:.2f} - 养老企业 {:.2f} - 失业个人 {:.2f} - 失业企业 {:.2f} - 医疗个人 {:.2f} - 医疗企业 {:.2f} - 年金个人 {:.2f} - 年金企业 {:.2f} - 生育企业 {:.2f} - 工伤企业 {:.2f}'.format(self.period, self.depart, self.numofpers, self.totalpayable, self.pay, self.tex, self.gjj_gr, self.gjj_qy, self.yl_gr, self.yl_qy, self.sy_gr, self.sy_qy, self.yil_gr, self.yil_qy, self.nj_gr, self.nj_qy, self.shy_qy, self.gs_qy)

    def create_auditorinfos(self, period, gzm, jjm):
        auditorinfos = dict()
        numofpers = dict()
        for k, vs in gzm.items():
            mop = dict()
            for v in vs:
                mop[v._code] = PersonSalaryInfo(period, v._code, v, None)
            numofpers[k] = mop
        for k, vs in jjm.items():
            mop = dict()
            if k in numofpers:
                mop = numofpers[k]
            for v in vs:
                if v._code in mop:
                    person = mop[v._code]
                    person.jj = v
                    mop[v._code] = person
                else:
                    mop[v._code] = PersonSalaryInfo(period, v._code, None, v)
            numofpers[k] = mop

        for k, vs in numofpers.items():
            auditorinfo = AuditorInfo()
            auditorinfo.period = v._period
            auditorinfo.depart = k
            auditorinfo.numofpers = len(vs)
            for c, v in vs.items():
                if v._gz is not None:
                    auditorinfo.totalpayable += v._gz._totalPayable
                    auditorinfo.pay += v._gz._pay
                    auditorinfo.tex += 0 - v._gz._gts
                    auditorinfo.gjj_gr += 0 - v._gz._gjj_bx
                    auditorinfo.gjj_qy += 0 - v._gz._gjj_qybx
                    auditorinfo.yl_gr += 0 - v._gz._yl_bx
                    auditorinfo.yl_qy += 0 - v._gz._yl_qybx
                    auditorinfo.sy_gr += 0 - v._gz._sy_bx
                    auditorinfo.sy_qy += 0 - v._gz._sy_qybx
                    auditorinfo.yil_gr += 0 - v._gz._yil_bx
                    auditorinfo.yil_qy += 0 - v._gz._yil_qybx
                    auditorinfo.nj_gr += 0 - v._gz._nj_bx
                    auditorinfo.nj_qy += 0 - v._gz._nj_qybx
                    auditorinfo.shy_qy += 0 - v._gz._shy_qybx
                    auditorinfo.gs_qy += 0 - v._gz._gs_qybx
                    auditorinfos[k] = auditorinfo
                if v._jj is not None:
                    auditorinfo.totalpayable += v._jj._totalPayable
                    auditorinfo.pay += v._jj._pay
                    auditorinfo.tex += 0 - v._jj._gts + 0 - v._jj._gstz
            auditorinfos[k] = auditorinfo
        return auditorinfos
