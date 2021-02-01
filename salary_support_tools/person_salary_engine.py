#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_salary_engine.py
@Time    :   2021/01/29 10:33:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import isfile, exists
from os import makedirs, listdir, remove

from collections import OrderedDict


class PersonSalaryEngine(object):

    def __init__(self, period, persons, gzs, jjs, banks):
        self._name = "person_salary"
        self._period = period  # 期间
        self._gzs = gzs   # 工资
        self._jjs = jjs  # 奖金
        self._persons = persons  # 人员信息集合
        self._banks = banks  # 银行信息
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        """
        组装人员的薪酬信息 包括 persons code depart
        """
        datas = self.merge_salary_person_bank_info(
            self._persons, self._banks, self.merge_salary_info(self._gzs, self._jjs))
        _, err_msgs = self.validate(datas)
        sap_datas = self.to_sap_info(datas)
        # self.err_info_write_to_depart_folder(err_msgs)
        return err_msgs, datas, sap_datas

    def merge_salary_info(self, gzs, jjs):
        # 根据单位分组工资奖金数据
        infos = OrderedDict()
        for gz in gzs:
            code = gz._code
            info = PersonSalaryInfo()
            info._period = self._period  # 期间信息
            info._depart = gz.depart  # 单位信息
            info._tex_depart = gz.tex_depart  # 税务机构
            info._gz = gz  # 工资信息
            vs = OrderedDict()
            if info._depart in infos:
                vs = infos[info._depart]
            vs[code] = info
            infos[info._depart] = vs
        for jj in jjs:
            code = jj._code
            jj_depart_str = jj.depart
            vs = OrderedDict()
            if jj_depart_str in infos:
                vs = infos[jj_depart_str]
            info = PersonSalaryInfo()
            if code in vs:
                info = vs[code]
            else:
                info._period = self._period  # 期间信息
                info._depart = jj.depart  # 单位信息
                info._tex_depart = jj.tex_depart  # 税务机构
            info._jj = jj  # 奖金信息
            vs[code] = info
            infos[info._depart] = vs
        return infos

    def merge_salary_person_bank_info(self, persons, banks, person_salary_infos):
        # 合并人员数据
        for depart_str, psis in person_salary_infos.items():
            for code, psi in psis.items():
                person, person_flag = self.get_person(code, persons)
                if person is not None:
                    psi._person = person
                    psi._person_flag = person_flag
                if depart_str in banks:
                    banks_info = banks[depart_str]
                    if code in banks_info:
                        bs = banks_info[code]
                        psi._banks = bs
        return person_salary_infos

    def get_person(self, code, persons):
        person = None
        if code in persons["c"]:  # 当前人员信息
            person = persons["c"][code]
            return person, "c"
        elif code in persons["o"]:  # 上期人员信息
            person = persons["o"][code]
            return person, "o"
        elif code in persons["o_o"]:
            person = persons["o"][code]
            return person, "o_o"
        else:
            return person, "n"

    def validate(self, person_salary_infos):
        """
        验证工资数据，验证奖金数据
        """
        # 验证工资
        #  实发 < 0
        #  缺少工资账号
        #  岗位绩效  缺少岗位工资
        #  生活费   岗位工资不为0
        err_mgs = dict()
        for depart, psis in person_salary_infos.items():
            err_message = []
            for code, person_salary_info in psis.items():
                person = person_salary_info._person
                gz = person_salary_info._gz
                jj = person_salary_info._jj
                banks = person_salary_info._banks
                if gz is not None:
                    # 实发小于0
                    if gz._pay < 0:
                        err_message.append(self.err_mss(
                            "工资信息错误", "工资实发小于0，实发金额{}".format(gz._pay), person))
                    # 缺少工资银行卡号
                    if gz._pay > 0:
                        if banks is None or banks["gz"] is None:
                            err_message.append(self.err_mss(
                                "银行卡信息错误", "缺少工资卡信息", person))
                    # 缺少岗位工资
                    if gz._salaryModel.startswith("岗位绩效工资制") and gz._gwgz == 0:
                        err_message.append(self.err_mss(
                            "工资信息错误", "岗位工资异常：缺少岗位工资信息", person))
                if jj is not None:
                    # 实发小于0
                    if jj._pay < 0:
                        err_message.append(self.err_mss(
                            "奖金信息错误", "奖金实发小于0，实发金额{}".format(gz._pay), person))
                    # 缺少工资银行卡号
                    if jj._pay > 0:
                        if banks is None or banks["jj"] is None:
                            err_message.append(self.err_mss(
                                "银行卡信息错误", "缺少奖金卡信息", person))
            if len(err_message) > 0:
                err_mgs[depart] = err_message

        return len(err_mgs) > 0, err_mgs

    def err_mss(self, err_type, message, person) -> str:
        if person is not None:
            return '错误信息提示:  ->  错误类型 {} - 错误信息 {} - 错误人员 {}'.format(err_type, message, person)
        return '错误信息提示:  ->  错误类型 {} - 错误信息 {}'.format(err_type, message)

    def to_sap_info(self, datas):
        res = dict()
        for depart, psis in datas.items():
            vs = dict()
            for code, psi in psis.items():
                ssi = SapSalaryInfo(psi._period, psi.salary_scope())
                ssi.to_sap(psi)
                vs[code] = ssi
            res[depart] = vs
        return res

    def err_info_write_to_depart_folder(self, errs_mgs):
        """
        写入相应得文件夹
        """
        for i, v in errs_mgs.items():
            path = r'{}\{}\{}\{}'.format(
                self._folder_prefix, self._period, i, "错误信息.txt")
            if exists(path):
                remove(path)
            if len(v) > 0:
                with open(path, 'a', encoding='utf-8') as f:
                    for i in range(len(v)):
                        msg = v[i]
                        f.write('{} {}'.format(i+1, msg + '\n'))
        return errs_mgs


class PersonSalaryInfo(object):
    """
    个人薪酬信息
    """

    def __init__(self, period="", depart="", person=None, code="", gz=None, jj=None, banks=None):
        self._period = period
        self._depart = depart
        self._tex_depart = ""  # 税务机构
        self._code = code
        self._gz = gz
        self._jj = jj
        self._banks = banks
        self._person = person
        self._person_flag = "c"  # "current"

    def salary_scope(self):
        if self._depart != "":
            return self._depart.split("_")[0]
        return ""


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

    def to_sap(self, person_salary_info: PersonSalaryInfo):
        personinfo = person_salary_info._person
        gzinfo = person_salary_info._gz
        jjinfo = person_salary_info._jj
        bankinfo = person_salary_info._banks
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
