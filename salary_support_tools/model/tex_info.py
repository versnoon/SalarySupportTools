#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_info.py
@Time    :   2021/02/22 14:51:20
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.sap_salary_info import SapSalaryInfo


class TexInfo:

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
        self._totalpayable = sapinfo.get_totalable()     # 本期收入
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
        self._bz = '{}-{}'.format(sapinfo.one, sapinfo.depart)  # 备注

    def to_tex_special(self, sapinfo: SapSalaryInfo):
        self._code = sapinfo._code  # 工号
        self._name = sapinfo._name  # *姓名
        self._idno = sapinfo._idno  # 证件号码
        self._totalpayable = sapinfo._nddxj  # 年底对象奖
        self._bz = '{}-{}'.format(sapinfo.one, sapinfo.depart)
