#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_operator.py
@Time    :   2021/02/01 19:00:02
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from os.path import exists
from os import remove, makedirs

import xlwt

from salary_support_tools.person_salary_engine import SapSalaryInfo
from salary_support_tools.tex_engine import TexSysStruct


class TexExport(object):

    """
    # 所得税相关表格输出
    # 1 输出宝武ehr数据
    # 2 输出所得税系统数据
    # 3 输出核对结果
    """

    def __init__(self, period, sap_salary_infos, tex_datas, err_msgs):
        self._period = period
        self._folder_path = r'd:\薪酬审核文件夹'
        self._sap_salary_infos = sap_salary_infos  # sap数据格式
        self._tex_datas = tex_datas
        self._err_msgs = err_msgs
        self._exportable = False

    def export(self):
        # 输出宝武数据
        self.export_ehr_datas_to_excel()
        # 输出所得税系统数据
        self.export_tex_datas_to_excel()
        # 输出核对结果信息
        self.err_info_write_to_depart_folder()

    def err_info_write_to_depart_folder(self):
        """
        写入相应得文件夹
        """
        for vs in self._err_msgs.values():
            for i, v in vs.items():
                path = r'{}\{}\{}\{}'.format(
                    self._folder_path, self._period, i, "个税核对结果.txt")
                if exists(path):
                    remove(path)
                if len(v) > 0:
                    with open(path, 'a', encoding='utf-8') as f:
                        for i in range(len(v)):
                            msg = v[i]
                            f.write('{} {}'.format(i+1, msg + '\n'))

    def export_ehr_datas_to_excel(self):
        """
        创建excel
        """
        for depart, vs in self._sap_salary_infos.items():
            if not self.exportable(depart):
                continue
            b = xlwt.Workbook(encoding='uft-8')
            s = b.add_sheet('正常工资薪金收入')

            source = []
            columndefs = self.import_tpl_columns()
            for v in vs.values():
                ti = TexInfo()
                ti.to_tex(v)
                source.append(ti)
                # 写入标题
            for i, v in enumerate(columndefs.values()):
                s.write(0, i, v)
            for i, v in enumerate(source):
                for j, propertyName in enumerate(columndefs.keys()):
                    try:
                        s.write(
                            i+1, j, getattr(source[i], propertyName, ''))
                    except TypeError:
                        print(propertyName)
            path = r'{}\{}\{}\导出文件'.format(
                self._folder_path, self._period, depart)
            if not exists(path):
                makedirs(path)
            b.save(r'{}\{}_{}_{}'.format(
                path, depart, self._period, "正常工资薪金所得.xls"))

    def export_tex_datas_to_excel(self):
        for tex_depart, vsm in self._tex_datas.items():
            for depart, vs in vsm.items():
                if not self.exportable(depart):
                    continue
                b = xlwt.Workbook(encoding='uft-8')
                s = b.add_sheet('综合所得申报税款计算')

                source = vs
                columndefs = self.export_tpl_columns()
                # 写入标题
                for i, v in enumerate(columndefs.values()):
                    s.write(0, i, v)
                for i, v in enumerate(source):
                    for j, propertyName in enumerate(columndefs.keys()):
                        try:
                            s.write(
                                i+1, j, getattr(source[i], propertyName, ''))
                        except TypeError:
                            print(propertyName)
                path = r'{}\{}\{}\导出文件'.format(
                    self._folder_path, self._period, depart)
                if not exists(path):
                    makedirs(path)
                b.save(r'{}\{}_{}_{}'.format(
                    path, depart, self._period, "综合所得申报税款计算.xls"))

    def import_tpl_columns(self):
        """
        所得税系统导入模板对应关系
        """
        columns = dict()
        columns["_code"] = "工号"
        columns["_name"] = "*姓名"
        columns["_certificateType"] = "*证件类型"
        columns["_idno"] = "*证件号码"
        columns["_totalpayable"] = "本期收入"
        columns["_notexpay"] = "本期免税收入"
        columns["_yl"] = "基本养老保险费"
        columns["_yil"] = "基本医疗保险费"
        columns["_sy"] = "失业保险费"
        columns["_gjj"] = "住房公积金"
        columns["_znjj"] = "累计子女教育"
        columns["_jxjj"] = "累计继续教育"
        columns["_zfdkll"] = "累计住房贷款利息"
        columns["_zfzj"] = "累计住房租金"
        columns["_ljsylr"] = "累计赡养老人"
        columns["_nj"] = "企业(职业)年金"
        columns["_syjkx"] = "商业健康保险"
        columns["_syylbx"] = "税延养老保险"
        columns["_qt"] = "其他"
        columns["_zykc"] = "准予扣除的捐赠额"
        columns["_jmse"] = "减免税额"
        columns["_bz"] = "备注"
        return columns

    def export_tpl_columns(self):
        """
        所得税系统导入模板对应关系
        """
        return TexSysStruct().getColumnDef()

    def exportable(self, depart):
        for vss in self._err_msgs.values():  # 如果有错误信息就跳过
            if depart in vss:
                return False or self._exportable
        return True


class TexInfo(object):
    """
    所得税相关信息定义
    """

    def __init__(self):
        self._code = ""  # 工号
        self._name = ""  # *姓名
        self._certificateType = "居民身份证"  # *证件类型
        self._idno = ""  # 证件号码
        self._totalpayable = 0  # 本期收入
        self._notexpay = None  # 本期免税收入
        self._yl = 0  # 基本养老保险费
        self._yil = 0  # 基本医疗保险费
        self._sy = 0  # 基本失业保险费
        self._gjj = 0  # 住房公积金
        self._znjj = None  # 累计子女教育
        self._jxjj = None  # 累计继续教育
        self._zfdkll = None  # 累计住房贷款利息
        self._zfzj = None  # 累计住房租金
        self._ljsylr = None  # 累计赡养老人
        self._nj = 0  # 企业（职业）年金
        self._syjkx = None  # 商业健康保险
        self._syylbx = None  # 税延养老保险
        self._qt = None  # 其他
        self._zykc = None  # 准予扣除的捐赠额
        self._jmse = None  # 减免税额
        self._bz = ""  # 备注

    def to_tex(self, sapinfo: SapSalaryInfo):
        self._code = sapinfo._code  # 工号
        self._name = sapinfo._name  # *姓名
        self._idno = sapinfo._idno  # 证件号码
        self._totalpayable = sapinfo._totalpayable + \
            sapinfo._gjj - 2410 + sapinfo._nj - 804  # 本期收入
        self._yl = sapinfo._yl  # 基本养老保险费
        if sapinfo._yl < 0:
            self._yl = 0
        self._yil = sapinfo._yil  # 基本医疗保险费
        if sapinfo._yil < 0:
            self._yil = 0
        self._sy = sapinfo._sy  # 基本失业保险费
        if sapinfo._sy < 0:
            self._sy = 0
        self._gjj = sapinfo._gjj  # 住房公积金
        if sapinfo._gjj > 2410:
            self._gjj = 2410  # 住房公积金
        self._nj = sapinfo._nj  # 企业（职业）年金
        if sapinfo._nj > 804:
            self._nj = 804
        if sapinfo._nj < 0:
            self._nj = 0
        self._bz = '{}-{}'.format(sapinfo.one, sapinfo.two)  # 备注
