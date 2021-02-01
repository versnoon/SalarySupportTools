#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine.py
@Time    :   2021/01/19 13:56:33
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import isfile, exists, join
from os import makedirs, walk, listdir


from collections import OrderedDict

from collections import defaultdict

import xlrd
import xlwt

from salary_support_tools.person_engine import PersonEngine, PersonInfo

from salary_support_tools.exl_to_clazz import ExlToClazz, ExlsToClazz

from salary_support_tools.salary_period_engine import SalaryPeriodEngine
from salary_support_tools.salary_depart_engine import SalaryDepartEngine
from salary_support_tools.salary_bank_engine import SalaryBankInfo
from salary_support_tools.salary_gz_engine import SalaryGzEngine, SalaryGzInfo
from salary_support_tools.salary_jj_engine import SalaryJjEngine, SalaryJjInfo


class EhrEngine(object):
    """
    ehr相关操作
    """

    def __init__(self, name='ehr'):
        self._name = name
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self, persons, period, departs, banks):
        """
        docstring
        """
        # 循环处理单位信息
        for v in departs.values():
            datas, depart = self.parserInfos(persons, period, v, banks)
            self.export_sap_info(datas, period, depart)

    def parserInfos(self, persons, period, salaryDepart, banks):
        """
        将ehr数据转换为Sap相关格式数据并导出

        """
        # 单位文件夹名称
        depart = '{}_{}'.format(salaryDepart.salaryScope, salaryDepart.name)

        # 解析人员工资信息
        gz_engine = SalaryGzEngine(period, depart)
        salaryGzs = gz_engine.start()

        # 解析人员奖金信息
        jj_engine = SalaryJjEngine(period, depart)
        salaryJjs = jj_engine.start()

        so = SapsOperator(period, salaryDepart, persons,
                          salaryGzs, salaryJjs, banks)
        datas = so.to_saps()
        return datas, depart

    def validate(self, persinfos, salaryGzs, salaryJjs, salaryBanks):
        """
        验证员工的相关信息
        """
        # 验证工资数据
        for gz in salaryGzs:
            code = gz._code
            # 工资奖金实发小于0
            if gz._pay < 0:
                print("{}，工资实发 < 0 {}".format(persinfos[code], gz._pay))
            # 缺少银行卡号
            if salaryBanks[code]['gz'] is None:
                print("{}，缺少工资银行信息".format(persinfos[code]))
        for jj in salaryJjs:
            code = jj._code
            # 工资奖金实发小于0
            if gz._pay < 0:
                if code in persinfos:
                    print("{}，奖金实发 < 0 {}".format(persinfos[code], gz._pay))
            # 缺少银行卡号
            if salaryBanks[code]['jj'] is None:
                print("{}，缺少奖金银行信息".format(persinfos[code]))

            # 所得税核对
            # 社保核对 怎么完成核对逻辑

    def export_sap_info(self, datas, period, depart):
        """
        生成各类所需的拨款单，银行报盘 等
        """
        if len(datas) > 0:
            ao = AuditerOperator(datas, period, depart)
            ao.export()
            sh = ReportOperator(datas, period, depart)
            sh.export()
            sh003 = ReportSh003Operator(datas, period, depart)
            sh003.export()


class SapsOperator(object):
    """
    转换成sap格式
    """

    def __init__(self, period, salaryDepart, personinfos, salaryGzs, salaryJjs, salaryBanks):
        self.period = period
        self.salaryDepart = salaryDepart
        self._persons = personinfos
        self._gzs = salaryGzs
        self._jjs = salaryJjs
        self._banks = salaryBanks

    def to_saps(self):
        datas = []
        # 工资奖金数据
        for key in self._gzs.keys():
            a = SapSalaryInfo(self.period, self.salaryDepart.salaryScope)
            jj = None
            if key in self._jjs:
                jj = self._jjs[key]
            bank = None
            if key in self._banks[self.salaryDepart.get_depart_salaryScope_and_name()]:
                bank = self._banks[self.salaryDepart.get_depart_salaryScope_and_name(
                )][key]
                a.to_sap(self._persons[key],
                         self._gzs[key], jj, bank)
            datas.append(a)
        # 其他不在系统内人员
        for key in self._jjs.keys():
            # 向往期找信息
            if key not in self._gzs:
                a = SapSalaryInfo(self.period, self.salaryDepart.salaryScope)
                bank = None
                if key in self._banks[self.salaryDepart.get_depart_salaryScope_and_name()]:
                    bank = self._banks[self.salaryDepart.get_depart_salaryScope_and_name(
                    )][key]
                    a.to_sap(None, None, self._jjs[key], bank)
                #
                if a.one is None or a.one == "" or len(a.one) == 0:
                    # 减员人员机构信息从奖金机构信息中获取
                    jj = self._jjs[key]
                    departs = jj._departfullinfo.split("\\")
                    if len(departs) > 0:
                        a.one = departs[0]
                    if len(departs) > 1:
                        a.two = departs[1]
                    if len(departs) > 2:
                        a.three = departs[2]
                    if len(departs) > 3:
                        a.four = departs[3]
                    if len(departs) > 4:
                        a.five = departs[4]

                datas.append(a)
        return datas


class AuditerOperator(object):
    """
    审核表相关业务
    """

    def __init__(self, datas, period, depart):
        self.period = period
        self.depart = depart
        self.datas = datas

    def export(self):
        # 导出excel
        self.createExcel(self.datas, self.columnsDef())

    def columnsDef(self):
        columns = OrderedDict()
        columns["period"] = "发薪期间"
        columns["salaryScope"] = "工资范围"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbz"] = "生活补助"
        columns["_khgz"] = "考核工资"
        columns["_gzbt"] = "工资补退"
        columns["_qtgz"] = "其他工资"
        columns["_ntjbgz"] = "内退基本工资"
        columns["_ntzz"] = "内退增资"
        columns["_ntglgz"] = "内退工龄工资"
        columns["_djsj"] = "代缴三金"
        columns["_wjbt"] = "物价补贴"
        columns["_ybjt"] = "夜班津贴"
        columns["_jsjt"] = "技师津贴"
        columns["_yzdnjt"] = "一专多能工津贴"  # 包含 计生 纪检 津贴
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"
        columns["_totaljj"] = "奖金合计"
        columns["_totaljbf"] = "加班费合计"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_yil"] = "医疗保险缴"
        columns["_sy"] = "失业保险"
        columns["_yl_bj"] = "养老保险补缴"
        columns["_yil_bj"] = "医疗保险补缴"
        columns["_sy_bj"] = "失业保险补缴"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_cwkk"] = "财务扣款"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "收视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费用"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "防暑降温"
        columns["_hm"] = "回民"
        columns["_jj"] = "纪检津贴"
        columns["_js"] = "计生津贴"
        columns["_wc"] = "误餐补贴"
        columns["_ksryj"] = "矿山荣誉金"
        columns["_xf"] = "信访津贴"
        columns["_scjt"] = "伤残津贴"
        columns["_zwbt"] = "职务补贴"
        columns["_kyxm"] = "科研项目津贴"
        columns["_jsgg"] = "技术攻关津贴"
        columns["_fgzjtbf"] = "非工资性津贴补发"

        columns["_totalpayable"] = "工资应发"
        columns["_totalpay"] = "实发工资"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "上卡效益奖"
        columns["_gsxyjtex"] = "效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年终奖实发"
        columns["_nddxjtex"] = "年终奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_sfhd"] = "实发核对"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["_err01"] = "事假旷工天数"
        columns["_err02"] = "病假天数"

        return columns

    def createExcel(self, datas, columndefs):
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

        path = r'd:\薪酬审核文件夹\{}\{}\导出文件'.format(self.period, self.depart)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}_{}_{}'.format(path, self.depart, self.period, "审核表数据.xls"))


class SapSalaryInfo(object):
    """
    SAP模型
    """

    def __init__(self, period, salaryScope, code="", name="", gwgz=0, blgz=0, nggz=0, fzgz=0, shbz=0, khgz=0, gzbt=0, qtgz=0, ntjbgz=0, ntzz=0, ntglgz=0, djsj=0, ybjt=0, jsjt=0, yzdnjt=0, ksjt=0, xjjt=0, zwjt=0, wyjt=0, bzzjt=0, kjjt=0, nsjt=0, totaljbf=0, totalqq=0, gjj=0, yl=0, sy=0, yil=0, nj=0, totalsdj=0, sljj=0, cwkk=0, cwbt=0, wybt=0, bjf=0, db=0, txf=0, gwf=0, hm=0, wcf=0, scjt=0, zwbt=0, kyxm=0, jsgg=0, fgzjtbf=0, yznx=0, totalpayable=0, totalpay=0, jyjf=0, gcjt=0, jssc=0, qt=0, jbjj=0, gsxyj=0, nddxj=0, nddxjpay=0, nddxjtex=0, jsjj=0, totaljj=0, gzpay=0, jjpay=0, bankno1="", bankinfo1="", bankno2="", bankinfo2="", ygz=""):
        self.period = period  # 期间
        self.salaryScope = salaryScope  # 工资范围
        self.one = ""  # 一级组织
        self.two = ""  # 二级组织
        self.three = ""  # 三级组织
        self.four = ""  # 四级组织
        self.five = ""  # 五级组织
        self.rsfw = self.one  # 人事范围
        self.zw = ""  # 职位
        self.zz = ""  # 职族
        self._code = ""  # 职工编码
        self._name = ""  # 姓名
        self._idno = ""  # 身份证号
        # 工资信息
        self._gwgz = 0  # 岗位工资
        self._blgz = 0  # 保留工资
        self._nggz = 0  # 年功工资
        self._fzgz = 0  # 辅助工资
        self._shbz = 0  # 生活补助
        self._khgz = 0  # 考核工资
        self._gzbt = 0  # 工资补退
        self._qtgz = 0  # 其他工资
        self._ntjbgz = 0  # 内退基本工资
        self._ntzz = 0  # 内退增资
        self._ntglgz = 0  # 内退工龄工资
        self._djsj = 0  # 代缴三金
        self._wjbt = 0  # 物价补贴
        self._ybjt = 0  # 夜班津贴
        self._jsjt = 0  # 技师津贴
        self._yzdnjt = 0  # 一转多能津贴(纪检 计生 信访)
        self._ksjt = 0  # 矿山津贴
        self._xjjt = 0  # 下井津贴
        self._zwjt = 0  # 驻外津贴 （原教护龄津贴）
        self._hszjt = 0  # 护士长津贴
        self._wyjt = 0  # 外语津贴
        self._bzzjt = 0  # 班组长津贴
        self._kjjt = 0  # 科技津贴
        self._nsjt = 0  # 能手津贴
        self._totaljj = 0  # 奖金合计
        self._fd_jbf = 0  # 法定加班
        self._gxr_jbf = 0  # 公休日加班
        self._ps_jbf = 0  # 平时加班
        self._totaljbf = 0  # 加班费合计
        self._totalqq = 0  # 缺勤扣款合计
        self._yznx = 0  # 预支年薪
        self._zygz = 0  # 执业工资

        self._gjj = 0  # 公积金个人
        self._yl = 0  # 养老保险个人
        self._yl_bj = 0  # 养老保险个人补缴 00
        self._sy = 0  # 失业保险个人
        self._sy_bj = 0  # 失业保险个人补缴 =0
        self._yil = 0  # 医疗保险个人
        self._yil_bj = 0  # 医疗保险个人补缴=0
        self._nj = 0  # 年金保险个人

        # 其他扣缴
        self._sljj = 0  # 水利基金
        self._cwkk = 0  # 财务扣款

        self._df = 0  # 电费
        self._fz = 0  # 房租
        self._dsf = 0  # 电视费
        self._qjf = 0  # 清洁费
        self._ccf = 0  # 乘车费
        self._cwbt = 0  # 财务补退

        # 非工资信息
        self._wybt = 0  # 物业补贴
        self._bjf = 0  # 保健费
        self._db = 0  # 独补
        self._txf = 0  # 通讯费
        self._gwf = 0  # 高温津贴
        self._hm = 0  # 回民
        self._jj = 0  # 纪检津贴
        self._js = 0  # 计生津贴
        self._wcf = 0  # 误餐费
        self._ksryj = 0  # 矿山荣誉金
        self._xf = 0  # 信访津贴
        self._scjt = 0  # 伤残津贴
        self._zwbt = 0  # 职务补贴
        self._kyxm = 0  # 科研项目津贴
        self._jsgg = 0  # 技术攻关津贴
        self._fgzjtbf = 0  # 非工资津贴补发

        # 奖金信息
        self._jbjj = 0  # 基本奖金
        self._onejj = 0  # 单项奖1
        self._twojj = 0  # 单项奖2
        self._threejj = 0  # 单项奖3
        self._gsxyj = 0  # 公司效益奖
        self._gsxyjpay = 0  # 公司效益奖上卡
        self._gsxyjtex = 0  # 公司效益奖所得税
        self._nddxj = 0  # 年底兑现奖
        self._nddxjpay = 0  # 年底兑现将实发
        self._nddxjtex = 0  # 年底兑现将所得税
        self._jsjj = 0  # 计税奖金
        self._gcjt = 0  # 工程津贴
        self._jssc = 0  # 技术输出
        self._qt = 0  # 争取国家政策等
        # 账号信息
        self._bankno1 = ""  # 银行账号1
        self._bankinfo1 = ""  # 银行1
        self._bankno2 = ""  # 银行账号1
        self._bankinfo2 = ""  # 银行1

        # 汇总

        self._totalsdj = 0  # 所得税
        self._totalpayable = 0  # 应发
        self._totalpay = 0  # 实发
        self._gzpay = 0  # 工资上卡
        self._jjpay = 0  # 奖金上卡
        self._nddxjpay = 0  # 年终奖上卡
        self._sfhd = 0  # 实发核对

        # 代发项目

        self._jyjf = 0  # 教育经费
        self._gcjt = 0  # 工程津贴
        self._jssc = 0  # 技术输出
        self._qt = 0  # 其他

        self._ygz = ""  # 员工组
        self._ygzz = ""  # 员工自足

        self._znjy = 0  # 子女教育
        self._jxjy = 0  # 继续教育
        self._zfdk = 0  # 住房贷款
        self._zffz = 0  # 住房租金
        self._sylr = 0  # 赡养老人
        self._mggl = 0  # 马钢工龄
        self._gl = 0  # 参加工作时间工龄
        self._cwdf = 0  # 财务代发计税项
        self._cwdff = 0  # 财务代发非计税项
        self._ljyf = 0  # 累计应发
        self._ljwx = 0  # 累计五险
        self._ljqt = 0  # 累计其他
        self._ljjm = 0  # 累计减免
        self._ljtex = 0  # 累计个税

    def to_sap(self, personinfo: PersonInfo, gzinfo: SalaryGzInfo, jjinfo: SalaryJjInfo, bankinfo: SalaryBankInfo):
        if personinfo is not None:
            self.one = personinfo._complayLevelOne
            self.two = personinfo._departLevelTow
            self.three = personinfo._branchLevelThree
            self.four = personinfo._assignmentSectionLevelFour
            self.five = personinfo._groupLevelFive

            self._code = personinfo._code
            self._name = personinfo._name
            self._ygz = personinfo._personType
            self._ygzz = personinfo._jobStatus

            self.zw = personinfo._cJobTitle
            self.zz = personinfo._postType

            self._mggl = personinfo._timeOfJoinBaowu  # 进宝武时间
            self._gl = personinfo._timeOfWork  # 参加工作时间
            self._idno = personinfo._idNo

        else:
            if jjinfo is not None:
                self._code = jjinfo._code
                self._name = jjinfo._name
            else:
                raise ValueError("数据异常，存在不合法的发放人员数据")
        if gzinfo is not None:
            self._gwgz = gzinfo._gwgz
            # 直管领导 岗位薪 统计在岗位工资上
            if gzinfo._gwx > 0 and gzinfo._gwgz == 0:
                self._gwgz = gzinfo._gwx
            # 直管领导 资历薪 统计在保留工资上
            self._blgz = gzinfo._blgz
            if gzinfo._zlx > 0 and gzinfo._blgz == 0:
                self._blgz = gzinfo._zlx
            self._nggz = gzinfo._glgz
            self._fzgz = gzinfo._qtblgz
            self._shbz = gzinfo._shbt_jt
            self._khgz = gzinfo._khfd
            self._gzbt = gzinfo._gztz
            self._qtgz = gzinfo._shf
            self._ntjbgz = gzinfo._gdgz
            self._ntzz = gzinfo._dtxgz
            self._ntglgz = 0
            self._djsj = gzinfo._shfbc_jt
            self._wjbt = 0
            self._ybjt = gzinfo._zyb_jt
            self._jsjt = gzinfo._jn_jt
            self._yzdnjt = gzinfo._jggz_jt
            self._ksjt = 0
            self._xjjt = 0
            self._zwjt = gzinfo._zw_jt
            self._wyjt = gzinfo._xl_jt
            self._bzzjt = gzinfo._gzz_jt
            self._kjjt = gzinfo._kjyx_jt
            self._nsjt = gzinfo._czns_jt
            self._fd_jbf = gzinfo._fd_jbgz
            self._gxr_jbf = gzinfo._xxr_jbgz
            self._ps_jbf = gzinfo._ps_jbgz

            self._totaljbf = gzinfo._total_jbgz
            self._totalqq = gzinfo._total_kk

            self._gjj = 0 - gzinfo._gjj_bx
            self._yl = 0 - gzinfo._yl_bx
            self._sy = 0 - gzinfo._sy_bx
            self._yil = 0 - gzinfo._yil_bx
            self._nj = 0 - gzinfo._nj_bx

            if gzinfo._gts != "":
                self._totalsdj = 0 - gzinfo._gts  # 工资所得税

            if gzinfo._qtdkk != "":
                self._sljj = 0 - gzinfo._qtdkk  # 水利基金
            if gzinfo._qtkk != "":
                self._cwkk = gzinfo._qtkk  # 其他扣款

            self._cwbt = gzinfo._qtbf + gzinfo._bfone  # 财务补退

            self._wybt = gzinfo._sdqnwy_jt  # 物业补贴
            self._bjf = gzinfo._cq_jt
            self._db = gzinfo._dsznf
            self._txf = gzinfo._tx_jt
            self._gwf = gzinfo._gw_jt
            self._hm = gzinfo._mz_jt
            self._wcf = gzinfo._wc_jt
            self._scjt = gzinfo._gs_jt
            self._zwbt = gzinfo._gongw_jt
            self._kyxm = gzinfo._tsgx_jt
            self._jsgg = gzinfo._js_jt
            self._fgzjtbf = gzinfo._gexbt_jt
            self._yznx = gzinfo._ygdxz + gzinfo._jxgz + gzinfo._yfjxnx
            self._znjy = gzinfo._znjyZxkc
            self._jxjy = gzinfo._jxjyZxkc
            self._zfdk = gzinfo._fdZxkc
            self._zffz = gzinfo._fzZxkc
            self._sylr = gzinfo._sylrZxkc

            self._cwdf = gzinfo._qtnssr  # 其他纳税收入

            self._totalpayable = gzinfo._totalPayable + gzinfo._dsznf    # 工资应发 独补合计
            self._totalpay = gzinfo._pay - gzinfo._jkdjf  # 工资实发
            self._gzpay = gzinfo._pay - gzinfo._jkdjf  # 工资实发 - 教育经费

            self._jyjf = gzinfo._jkdjf

        if jjinfo is not None:
            self._jbjj = jjinfo._jbjj
            self._onejj = jjinfo._bonusOne
            self._twojj = jjinfo._bonusTwo
            self._threejj = jjinfo._bonusThree

            self._gcjt = jjinfo._gcjj
            self._jssc = jjinfo._jssc
            self._qt = jjinfo._qt
            self._gsxyj = jjinfo._gsxyj
            self._nddxj = jjinfo._nddxj
            self._jsjj = jjinfo._jsjj

            self._totaljj = jjinfo._totalPayable

            self._totalsdj = self._totalsdj + 0 - jjinfo._gts + \
                0 - jjinfo._gstz  # 合并入奖金所得税(包括奖金个税调整)

            self._totalpayable = self._totalpayable + jjinfo._totalPayable  # 合并奖金应发
            self._totalpay = self._totalpay + jjinfo._pay  # 合并奖金实发
            self._jjpay = jjinfo._pay  # 奖金实发

        if bankinfo is not None:
            self._bankno1 = bankinfo['gz']._bankNo
            self._bankinfo1 = bankinfo['gz']._financialInstitution
            if 'jj' in bankinfo and bankinfo['jj'] is not None:
                self._bankno2 = bankinfo['jj']._bankNo
                self._bankinfo2 = bankinfo['jj']._financialInstitution

    def __str__(self):
        return '审批表信息: 发薪日期 {} - 工资范围 {} - 职工编码 {} - 姓名 {} - 人员类型 {} - 在职状态 {} - 应发合计 {} - 奖金合计 {} - 公积金 {} - 养老保险 {} - 失业保险 {} - 医疗保险 {} - 年金 {} - 所得税 {} - 实发合计 {} - 工资卡号 {} - 工资卡金融机构 {} - 奖金卡号 {} - 奖金卡金融机构 {}'.format(
            self.period, self.salaryScope, self._code, self._name, self._ygz, self._ygzz, self._totalpayable, self._totaljj, self._gjj, self._yl, self._sy, self._yil, self._nj, self._totalsdj, self._totalpay, self._bankno1, self._bankinfo1, self._bankno2, self._bankinfo2)


class ReportOperator(object):
    '''
    报表格式数据导出
    '''

    def __init__(self, datas, period, depart):
        self.datas = datas
        self.period = period
        self.depart = depart

    def export(self):
        # 导出excel
        self.createExcel(self.datas, self.columnsDef())

    def columnsDef(self):
        columns = dict()
        columns["_sfhd"] = "实发核对"
        columns["one"] = "一级组织"
        columns["two"] = "二级组织"
        columns["three"] = "三级组织"
        columns["four"] = "四级组织"
        columns["five"] = "五级组织"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_idno"] = "身份证"
        columns["salaryScope"] = "工资范围"
        columns["rsfw"] = "人事范围"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["zw"] = "职位"
        columns["zz"] = "职族"

        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbz"] = "生活补助"
        columns["_khgz"] = "考核工资"
        columns["_gzbt"] = "工资补退"
        columns["_qtgz"] = "其他工资"
        columns["_ntjbgz"] = "内退基本工资"
        columns["_ntzz"] = "内退增资"
        columns["_ntglgz"] = "内退工龄工资"
        columns["_djsj"] = "代缴三金"
        columns["_wjbt"] = "物价补贴"
        columns["_ybjt"] = "夜班津贴"
        columns["_jsjt"] = "技师津贴"
        columns["_yzdnjt"] = "一专多能工津贴"
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"

        columns["_jbjj"] = "基本奖金"
        columns["_onejj"] = "单项奖1"
        columns["_twojj"] = "单项奖2"
        columns["_threejj"] = "单项奖3"
        columns["_fd_jbf"] = "法定节日加班工资"
        columns["_gxr_jbf"] = "公休日加班工资"
        columns["_ps_jbf"] = "平时加班工资"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_yil"] = "医疗保险缴"
        columns["_sy"] = "失业保险"
        columns["_yl_bj"] = "养老保险补缴"
        columns["_yil_bj"] = "医疗保险补缴"
        columns["_sy_bj"] = "失业保险补缴"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_cwkk"] = "财务扣款"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "收视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费用"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "防暑降温"
        columns["_hm"] = "回民"
        columns["_jj"] = "纪检津贴"
        columns["_js"] = "计生津贴"
        columns["_wc"] = "误餐补贴"
        columns["_ksryj"] = "矿山荣誉金"
        columns["_xf"] = "信访津贴"
        columns["_scjt"] = "伤残津贴"
        columns["_zwbt"] = "职务补贴"
        columns["_kyxm"] = "科研项目津贴"
        columns["_jsgg"] = "技术攻关津贴"
        columns["_fgzjtbf"] = "非工资性津贴补发"

        columns["_totalpayable"] = "工资应发"
        columns["_totalpay"] = "实发工资"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "上卡效益奖"
        columns["_gsxyjtex"] = "效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年终奖实发"
        columns["_nddxjtex"] = "年终奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"

        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_znjy"] = "子女教育"
        columns["_jxjy"] = "继续教育"
        columns["_zfdk"] = "住房贷款利息"
        columns["_zffz"] = "住房租金"
        columns["_sylr"] = "赡养老人"
        columns["_mggl"] = "马钢工龄"
        columns["_gl"] = "工龄"
        columns["_cwdf"] = "财务代发计税项"
        columns["_cwdff"] = "财务代发非计税项"
        columns["_ljyf"] = "累计应发"
        columns["_ljwx"] = "累计五险两金"
        columns["_ljqt"] = "累计其他计税"
        columns["_ljjm"] = "累计标准免税额"
        columns["_ljtex"] = "累计个税"

        return columns

    def createExcel(self, datas, columndefs):
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
                    if propertyName == "one":
                        s.write(
                            i + 1, j, "马钢集团")
                    elif propertyName == "two" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "one", 0))
                    elif propertyName == "three" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "two", 0))
                    elif propertyName == "four" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "three", 0))
                    elif propertyName == "five" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "four", 0))
                    else:
                        s.write(
                            i+1, j, getattr(datas[i], propertyName, 0))
                except TypeError:
                    print(propertyName)

        path = r'd:\薪酬审核文件夹\{}\{}\导出文件'.format(self.period, self.depart)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}_{}_{}'.format(
            path, self.depart, self.period, "SAPSH002.xls"))


class ReportSh003Operator(object):
    '''
    报表格式数据导出
    '''

    def __init__(self, datas, period, depart):
        self.datas = datas
        self.period = period
        self.depart = depart

    def export(self):
        # 导出excel
        self.createExcel(self.datas, self.columnsDef())

    def columnsDef(self):
        columns = dict()
        columns["_sfhd"] = "实发核对"
        columns["one"] = "一级组织"
        columns["two"] = "二级组织"
        columns["three"] = "三级组织"
        columns["four"] = "四级组织"
        columns["five"] = "五级组织"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_idno"] = "身份证"
        columns["salaryScope"] = "工资范围"
        columns["rsfw"] = "人事范围"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["zw"] = "职位"
        columns["zz"] = "职族"

        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbz"] = "生活补助"
        columns["_khgz"] = "考核工资"
        columns["_gzbt"] = "工资补退"
        columns["_qtgz"] = "其他工资"
        columns["_ntjbgz"] = "内退基本工资"
        columns["_ntzz"] = "内退增资"
        columns["_ntglgz"] = "内退工龄工资"
        columns["_djsj"] = "代缴三金"
        columns["_wjbt"] = "物价补贴"
        columns["_ybjt"] = "夜班津贴"
        columns["_jsjt"] = "技师津贴"
        columns["_yzdnjt"] = "一专多能工津贴"
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"

        columns["_jbjj"] = "基本奖金"
        columns["_onejj"] = "单项奖1"
        columns["_twojj"] = "单项奖2"
        columns["_threejj"] = "单项奖3"
        columns["_fd_jbf"] = "法定节日加班工资"
        columns["_gxr_jbf"] = "公休日加班工资"
        columns["_ps_jbf"] = "平时加班工资"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_yil"] = "医疗保险缴"
        columns["_sy"] = "失业保险"
        columns["_yl_bj"] = "养老保险补缴"
        columns["_yil_bj"] = "医疗保险补缴"
        columns["_sy_bj"] = "失业保险补缴"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_cwkk"] = "财务扣款"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "收视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费用"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "防暑降温"
        columns["_hm"] = "回民"
        columns["_jj"] = "纪检津贴"
        columns["_js"] = "计生津贴"
        columns["_wc"] = "误餐补贴"
        columns["_ksryj"] = "矿山荣誉金"
        columns["_xf"] = "信访津贴"
        columns["_scjt"] = "伤残津贴"
        columns["_zwbt"] = "职务补贴"
        columns["_kyxm"] = "科研项目津贴"
        columns["_jsgg"] = "技术攻关津贴"
        columns["_fgzjtbf"] = "非工资性津贴补发"

        columns["_totalpayable"] = "工资应发"
        columns["_totalpay"] = "实发工资"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "上卡效益奖"
        columns["_gsxyjtex"] = "效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年终奖实发"
        columns["_nddxjtex"] = "年终奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"

        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_znjy"] = "子女教育"
        columns["_jxjy"] = "继续教育"
        columns["_zfdk"] = "住房贷款利息"
        columns["_zffz"] = "住房租金"
        columns["_sylr"] = "赡养老人"
        columns["_mggl"] = "马钢工龄"
        columns["_gl"] = "工龄"
        columns["_cwdf"] = "财务代发计税项"
        columns["_cwdff"] = "财务代发非计税项"
        columns["_ljyf"] = "累计应发"
        columns["_ljwx"] = "累计五险两金"
        columns["_ljqt"] = "累计其他计税"
        columns["_ljjm"] = "累计标准免税额"
        columns["_ljtex"] = "累计个税"
        columns["period"] = "发薪期间"

        return columns

    def createExcel(self, datas, columndefs):
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
                    if propertyName == "one":
                        s.write(
                            i + 1, j, "马钢集团")
                    elif propertyName == "two" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "one", 0))
                    elif propertyName == "three" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "two", 0))
                    elif propertyName == "four" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "three", 0))
                    elif propertyName == "five" and getattr(datas[i], "one", 0) != "马钢（集团）控股有限公司(总部)":
                        s.write(
                            i + 1, j, getattr(datas[i], "four", 0))
                    else:
                        s.write(
                            i+1, j, getattr(datas[i], propertyName, 0))
                except TypeError:
                    print(propertyName)

        path = r'd:\薪酬审核文件夹\{}\{}\导出文件'.format(self.period, self.depart)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}_{}_{}'.format(
            path, self.depart, self.period, "SAPSH003.xls"))


# class TexOperator(object):
#     """
#     税单相关表
#     """

#     def __init__(self, datas, period, depart):
#         self.datas = datas
#         self.depart = depart
#         self.period = period

#     def export(self):
#         # 导出excel
#         self.createExcel(self.datas, self.columnsDef())

#     def columnsDef(self):
#         columns = dict()
#         columns["_code"] = "工号"
#         columns["_name"] = "*姓名"
#         columns["_certificateType"] = "*证件类型"
#         columns["_idno"] = "*证件号码"
#         columns["_totalpayable"] = "本期收入"
#         columns["_notexpay"] = "本期免税收入"
#         columns["_yl"] = "基本养老保险费"
#         columns["_yil"] = "基本医疗保险费"
#         columns["_sy"] = "失业保险费"
#         columns["_gjj"] = "住房公积金"
#         columns["_znjj"] = "累计子女教育"
#         columns["_jxjj"] = "累计继续教育"
#         columns["_zfdkll"] = "累计住房贷款利息"
#         columns["_zfzj"] = "累计住房租金"
#         columns["_ljsylr"] = "累计赡养老人"
#         columns["_nj"] = "企业(职业)年金"
#         columns["_syjkx"] = "商业健康保险"
#         columns["_syylbx"] = "税延养老保险"
#         columns["_qt"] = "其他"
#         columns["_zykc"] = "准予扣除的捐赠额"
#         columns["_jmse"] = "减免税额"
#         columns["_bz"] = "备注"
#         return columns

#     def createExcel(self, datas, columndefs):
#         """
#         创建excel
#         """
#         b = xlwt.Workbook(encoding='uft-8')
#         s = b.add_sheet('正常工资薪金收入')

#         source = []
#         for v in datas:
#             ti = TexInfo()
#             ti.to_tex(v)
#             source.append(ti)
#         # 写入标题
#         for i, v in enumerate(columndefs.values()):
#             s.write(0, i, v)
#         for i, v in enumerate(source):
#             for j, propertyName in enumerate(columndefs.keys()):
#                 try:
#                     s.write(
#                         i+1, j, getattr(source[i], propertyName, ''))
#                 except TypeError:
#                     print(propertyName)

#         path = r'd:\薪酬审核文件夹\{}\{}\导出文件'.format(self.period, self.depart)
#         if not exists(path):
#             makedirs(path)
#         b.save(r'{}\{}_{}_{}'.format(
#             path, self.depart, self.period, "正常工资薪金所得.xls"))
