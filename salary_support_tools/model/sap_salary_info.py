#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sap_salary_info.py
@Time    :   2021/02/20 14:43:57
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.person_salary import PersonSalaryInfo
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SapSalaryInfo(object):
    """
    SAP模型
    """

    def __init__(self):
        self.period = None  # 期间
        self.depart = ""  # 工资范围
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
        self._totalpayable_1 = 0  # 应发含独补
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
        self._gl = ""  # 参加工作时间工龄
        self._cwdf = 0  # 财务代发计税项
        self._cwdff = 0  # 财务代发非计税项
        self._ljyf = 0  # 累计应发
        self._ljwx = 0  # 累计五险
        self._ljqt = 0  # 累计其他
        self._ljjm = 0  # 累计减免
        self._ljtex = 0  # 累计个税
        self._tex_totalable = 0  # 综合当期收入
        self._tex = 0  # 当期综合个税
        self._tex_totalable_special = 0  # 当期一次性奖励收入
        self._tex_special = 0  # 当期一次性奖励税
        self._sfkk = 0  # 司法扣款
        self._zxj = 0  # 重点工作奖
        self._ryj = 0  # 荣誉类奖
        self._jyj = 0  # 员工精益改善奖
        self._cwbt_jcx = 0  # 财务补退经常性
        self._cwbt_qt = 0  # 其它财务补退
        self._dlj = 0  # 宝武集团单列奖励

    def depart_info(self, personinfo, gz, jj):
        one, two, three = "", "", ""
        one = "马钢（集团）控股有限公司(总部)"
        depart_fullname = ""
        if personinfo:
            if personinfo._complayLevelOne != "马钢（集团）控股有限公司(总部)":
                two = personinfo._complayLevelOne
                three = personinfo._departLevelTow
            else:
                two = personinfo._departLevelTow
                three = personinfo._branchLevelThree
        if not two:
            if gz:
                two = gz._departLevelTow
            if not two:
                if jj:
                    depart_fullname = jj._depart_fullname
                    if depart_fullname:
                        departs = depart_fullname.split("\\")
                        if len(departs) > 1:
                            if departs[0] != "马钢（集团）控股有限公司(总部)":
                                two = departs[0]
                            else:
                                two = departs[1]
        if not three:
            if gz:
                three = gz._branchLevelThree
            if not three:
                if jj:
                    depart_fullname = jj._depart_fullname
                    if depart_fullname:
                        departs = depart_fullname.split("\\")
                        if len(departs) > 2:
                            if departs[0] != "马钢（集团）控股有限公司(总部)":
                                three = departs[1]
                            else:
                                three = departs[2]

        return one, two, three

    def to_sap(self, person_salary_info: PersonSalaryInfo):
        personinfo = person_salary_info._person
        gzinfo = person_salary_info._gz
        jjinfo = person_salary_info._jj
        bankinfo = person_salary_info._banks
        job = person_salary_info._job
        texes = person_salary_info._texes
        self.period = person_salary_info.period.period
        self.depart = person_salary_info._depart
        self.one, self.two, self.three = self.depart_info(
            personinfo, gzinfo, jjinfo)
        if personinfo is not None:
            if personinfo._complayLevelOne != "马钢（集团）控股有限公司(总部)":
                # self.one = "马钢（集团）控股有限公司(总部)"
                # self.two = personinfo._complayLevelOne
                # self.three = personinfo._departLevelTow
                self.four = personinfo._branchLevelThree
                self.five = personinfo._assignmentSectionLevelFour
            else:
                # self.one = personinfo._complayLevelOne
                # self.two = personinfo._departLevelTow
                # self.three = personinfo._branchLevelThree
                self.four = personinfo._assignmentSectionLevelFour
                self.five = personinfo._groupLevelFive

            self._code = personinfo._code
            self._name = personinfo._name
            self._ygz = personinfo._personType
            self._ygzz = personinfo._jobStatus

            if job is not None:
                self.zw = job._zx_jobname
                self.zz = job._job_type

            self._mggl = personinfo._timeOfJoinBaowu  # 进宝武时间
            self._gl = personinfo._timeOfWork  # 参加工作时间
            self._idno = personinfo._idno

        else:
            if jjinfo is not None:
                self._code = jjinfo._code
                self._name = jjinfo._name
            else:
                pass
                # raise ValueError("数据异常，存在不合法的发放人员数据")
        if gzinfo is not None:
            self._sfkk = gzinfo._sfkk  # 司法扣款
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

            self._cwbt_jcx = gzinfo._bfone  # 财务补退经常性
            self._cwbt_qt = gzinfo._qtbf  # 其他财务补退

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

            self._totalpayable = gzinfo._totalPayable  # 工资应发合计
            self._totalpay = gzinfo._pay  # 工资实发
            self._gzpay = gzinfo._pay  # 工资实发 - 教育经费

            self._jyjf = gzinfo._jkdjf

        if jjinfo is not None:
            self._zxj = jjinfo._zxj
            self._ryj = jjinfo._ryj
            self._jyj = jjinfo._jyj
            self._dlj = jjinfo._dlj

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

            self._totalpayable = self._totalpayable + \
                jjinfo._totalPayable - jjinfo._nddxj  # 合并奖金应发并减去年底兑现奖
            self._totalpay = self._totalpay + jjinfo._pay  # 合并奖金实发
            self._jjpay = jjinfo._pay  # 奖金实发

        if bankinfo is not None:
            if 'gz' in bankinfo and bankinfo['gz'] is not None:
                self._bankno1 = bankinfo['gz']._bankNo
                self._bankinfo1 = bankinfo['gz']._financialInstitution
            if 'jj' in bankinfo and bankinfo['jj'] is not None:
                self._bankno2 = bankinfo['jj']._bankNo
                self._bankinfo2 = bankinfo['jj']._financialInstitution
        # 所得税系统信息
        if texes is not None:
            if "s_tex" in texes:
                self._tex_totalable = texes["s_tex"]._totalpayable
                self._tex = texes["s_tex"]._tex
            if "s_one_tex" in texes:
                self._tex_totalable_special = texes["s_one_tex"]._totalpayable
                self._tex_special = texes["s_one_tex"]._tex

    @property
    def audit_cwkk(self):
        return self._cwkk + self._sfkk

    def get_totalable(self):
        totalpayable = self._totalpayable + self._jyjf
        if self._cwdf != -55000 and self._cwdf != 55000:
            totalpayable += self._cwdf
        if self._yl < 0:
            totalpayable += 0 - self._yl
        if self._yil < 0:
            totalpayable += 0 - self._yil
        if self._sy < 0:
            totalpayable += 0 - self._sy
        if self._gjj > 2410:
            totalpayable += self._gjj - 2410
        if self._nj > 804:
            totalpayable += self._nj - 804
        if self._nj < 0:
            totalpayable += 0 - self._nj
        return totalpayable

    def get_total_kc(self):
        total = 0
        if self._yl < 0:
            total += 0
        else:
            total += self._yl
        if self._yil < 0:
            total += 0
        else:
            total += self._yil
        if self._sy < 0:
            total += 0
        else:
            total += self._sy
        if self._gjj > 2410:
            total += 2410
        else:
            total += self._gjj
        if self._nj > 804:
            total += 804
        elif self._nj < 0:
            total += 0
        else:
            total += self._nj

        return total

    def __str__(self):
        return 'SAP薪酬信息: 发薪日期 {} - 审核单位 {} - 职工编码 {} - 姓名 {} - 人员类型 {} - 在职状态 {} - 应发合计 {} - 奖金合计 {} - 公积金 {} - 养老保险 {} - 失业保险 {} - 医疗保险 {} - 年金 {} - 所得税 {} - 实发合计 {} - 工资卡号 {} - 工资卡金融机构 {} - 奖金卡号 {} - 奖金卡金融机构 {}'.format(
            self.period, self.depart, self._code, self._name, self._ygz, self._ygzz, self._totalpayable, self._totaljj, self._gjj, self._yl, self._sy, self._yil, self._nj, self._totalsdj, self._totalpay, self._bankno1, self._bankinfo1, self._bankno2, self._bankinfo2)
